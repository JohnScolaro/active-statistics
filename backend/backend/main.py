import dataclasses
import datetime as dt
import json
import logging
import os
import secrets
from typing import Any, Callable

import boto3
import sentry_sdk
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from mangum import Mangum
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table
from mypy_boto3_s3 import S3Client
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.renderers.speedscope import SpeedscopeRenderer
from requests.exceptions import HTTPError
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from stravalib.client import Client
from stravalib.exc import RateLimitExceeded
from stravalib.model import DetailedAthlete, SummaryActivity
from stravalib.util.limiter import DefaultRateLimiter

from backend.gui.gui import get_all_tabs, tab_tree
from backend.tabs.tab_group import TabGroup
from backend.tabs.tabs import Tab
from backend.utils.aws_lambda import manually_trigger_route_via_lambda
from backend.utils.dynamodb import (
    get_athlete_id_from_session_token,
    get_download_status_item_from_dynamo,
    get_user_data_row_for_athlete,
    save_download_status_to_dynamo,
    save_user_data_to_dynamo,
)
from backend.utils.environment_variables import evm
from backend.utils.routes import unauthorized_if_no_session_token
from backend.utils.s3 import (
    delete_athlete_data,
    save_summary_activities_to_s3,
)

# Check if the app is running in development mode
is_dev = os.getenv("ENVIRONMENT", "production") == "development"

if not is_dev:
    sentry_sdk.init(
        dsn=evm.get_sentry_server_dsn(),
        integrations=[AwsLambdaIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )

logger = logging.getLogger(__name__)

app = FastAPI(debug=not evm.is_production())
handler = Mangum(app)


USER_TABLE_NAME = "user-table"
DOWNLOAD_STATUS_NAME = "download-status-table"

dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb")
user_table: Table = dynamodb.Table(USER_TABLE_NAME)
download_status_table: Table = dynamodb.Table(DOWNLOAD_STATUS_NAME)

s3_client: S3Client = boto3.client("s3", region_name="ap-southeast-2")


def register_middlewares(app: FastAPI):
    @app.middleware("http")
    async def profile_request(request: Request, call_next: Callable):
        """Profile the current request

        Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
        with small improvements.

        """
        # we map a profile type to a file extension, as well as a pyinstrument profile
        # renderer
        profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
        profile_type_to_renderer = {
            "html": HTMLRenderer,
            "speedscope": SpeedscopeRenderer,
        }

        # if the `profile=true` HTTP query argument is passed, we profile the request
        # if request.query_params.get("profile", False):
        # The default profile format is speedscope
        profile_type = request.query_params.get("profile_format", "speedscope")

        # we profile the request along with all additional middlewares, by interrupting
        # the program every 1ms1 and records the entire stack at that point
        with Profiler(interval=0.001, async_mode="enabled") as profiler:
            print(request.url)
            response = await call_next(request)

        # we dump the profiling into a file
        extension = profile_type_to_ext[profile_type]
        renderer = profile_type_to_renderer[profile_type]()
        with open(
            f"{'.'.join(str(request.url).split('/')[-2:])}.{extension}", "w"
        ) as out:
            out.write(profiler.output(renderer=renderer))
        return response


# Turn this on if you want to profile endpoints.
# register_middlewares(app)


def get_frontend_base_url() -> str:
    return f"{evm.get_protocol()}://{evm.get_domain()}:{evm.get_frontend_port()}"


def get_backend_base_url() -> str:
    return f"{evm.get_protocol()}://{evm.get_domain()}:{evm.get_backend_port()}"


# Define allowed origins (your frontend's domain)
origins = [
    get_frontend_base_url(),  # Default URL of next.js's dev frontend for development
]

# Add CORSMiddleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/api/example_chart_data")
async def chart_data(request: Request) -> JSONResponse:
    current_file_dir_path = os.path.dirname(os.path.realpath(__file__))
    example_chart_data_path = os.path.join(
        current_file_dir_path, "static", "example_charts", "polyline_animation.json"
    )
    # Read the example file
    with open(example_chart_data_path, "r") as f:
        json_data = f.read()

    return json.loads(json_data)


@app.get("/api/authenticate")
async def authenticate(request: Request) -> Any:
    # Retrieve query parameters
    code: str = request.query_params["code"]
    scope: str = request.query_params["scope"]

    # Do some terrible scope checking.
    # If we aren't given permission to read activities, just return to index.
    if scope != "read,activity:read":
        return RedirectResponse("/?scope_incorrect=true")

    # Try the following. It can fail in a couple different ways, all due to
    # hitting the Strava rate limit.
    try:
        client = Client()
        token_response = client.exchange_code_for_token(
            client_id=evm.get_strava_client_id(),
            client_secret=evm.get_strava_client_secret(),
            code=code,
        )
        # Get the access token and immediately use that to get the athlete id.
        client.access_token = token_response["access_token"]
        athlete: DetailedAthlete = client.get_athlete()

        # Create a unique session token.
        session_token = secrets.token_urlsafe(32)

        # Save all these important secrets to dynamodb
        save_user_data_to_dynamo(user_table, session_token, athlete.id, token_response)

        # Redirect to home while setting cookies.
        redirect_url = f"{get_frontend_base_url()}/home" if is_dev else "/home"
        response = RedirectResponse(url=redirect_url)
        response.set_cookie(
            key="session_token",
            value=session_token,
            max_age=30 * 60,  # 30 mins
            httponly=True,
            secure=True,  # Ensure HTTPS is used in production.
        )
    except (HTTPError, RateLimitExceeded) as _:
        return RedirectResponse("/?rate_limit_exceeded=true")

    response.set_cookie(
        key="logged_in",
        value="true",
        max_age=30 * 60,  # 30 mins.
        secure=True,  # Ensure HTTPS is used in production.
    )
    return response


@dataclasses.dataclass
class SideMenuTabs:
    name: str
    key: str
    type: str
    items: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "key": self.key,
            "type": self.type,
            "items": self.items,
        }


@app.get("/api/tabs", dependencies=[Depends(unauthorized_if_no_session_token)])
async def get_tabs(request: Request) -> list[Any]:
    def expand_tabs(tabs: list[Tab | TabGroup]) -> list[Any]:
        json_tabs = []
        for tab in tabs:
            if isinstance(tab, TabGroup):
                json_tabs.append(tab_to_dict(tab, items=expand_tabs(tab.children)))
            else:
                json_tabs.append(tab_to_dict(tab, items=[]))
        return json_tabs

    def tab_to_dict(tab: Tab | TabGroup, items: list[Any] = []) -> dict[str, Any]:
        return SideMenuTabs(
            name=tab.name, key=tab.get_key(), type=tab.get_type(), items=items
        ).to_dict()

    return expand_tabs(tab_tree)


# Before the app starts, we want to generate all the routes for our tabs.
for tab in get_all_tabs():
    tab.generate_and_register_route(app, evm, user_table, s3_client)


# The data status connection is a websocket
@app.get("/api/data_status", dependencies=[Depends(unauthorized_if_no_session_token)])
async def data_status(
    request: Request, background_tasks: BackgroundTasks
) -> JSONResponse:
    session_token = request.cookies["session_token"]
    athlete_id = get_athlete_id_from_session_token(user_table, session_token)
    download_status_item = get_download_status_item_from_dynamo(
        download_status_table, athlete_id
    )

    if not download_status_item:
        delete_athlete_data(s3_client, athlete_id)
        trigger_download_data(session_token, background_tasks)
        return {"message": "Starting data download...", "downloaded": False}

    if download_status_item.error:
        delete_athlete_data(s3_client, athlete_id)
        trigger_download_data(session_token, background_tasks)
        return {
            "message": "Attempting to redownload data after an error.",
            "downloaded": False,
        }

    if download_status_item.complete:
        return {"message": "Data downloaded.", "downloaded": True}

    return {"message": download_status_item.status, "downloaded": False}


def trigger_download_data(
    session_token: str, background_tasks: BackgroundTasks
) -> None:
    """
    To make local development not shit, the app should just download data in a
    background task if running locally, but trigger a lambda if running in prod.
    """
    if evm.is_production():
        manually_trigger_route_via_lambda(
            "GET",
            "/api/download_data",
            cookies={"session_token": session_token},
        )
    else:
        background_tasks.add_task(download_data, session_token)


@app.get("/api/download_data", dependencies=[Depends(unauthorized_if_no_session_token)])
async def download_data_route(
    request: Request, background_tasks: BackgroundTasks
) -> None:
    # Check if there is data at all.
    try:
        session_token = request.cookies["session_token"]
        download_data(session_token)
    except Exception as e:
        save_download_status_to_dynamo(
            download_status_table,
            get_athlete_id_from_session_token(user_table, session_token),
            dt.datetime.now(dt.timezone.utc),
            "There was an error while trying to download your data. Please try again later.",
            error=True,
            complete=True,
        )
        logger.error("Exception while trying to download data.")
        logger.exception(e)


def download_data(session_token: str) -> None:
    print("Downloading user data...")
    athlete_id = get_athlete_id_from_session_token(user_table, session_token)
    print(f"Athlete ID is {athlete_id}")
    current_time_utc = dt.datetime.now(dt.timezone.utc)

    save_download_status_to_dynamo(
        download_status_table,
        athlete_id,
        current_time_utc,
        status="Starting download.",
        error=False,
        complete=False,
    )

    # Get required tokens.
    row = get_user_data_row_for_athlete(user_table, session_token)

    # Set the clients access token for the user.
    client = Client(access_token=row.access_token, rate_limiter=DefaultRateLimiter())

    summary_activities: list[SummaryActivity] = []
    i = 0

    # Iterate over the activities returned by the batched iterator
    for idx, activity in enumerate(client.get_activities(), start=1):
        summary_activities.append(activity)

        # Print the count every 200 activities
        if idx % 200 == 0:  # 200 is the default page size for the batched iterator
            print(f"{idx} activities downloaded so far.")
            save_download_status_to_dynamo(
                download_status_table,
                athlete_id,
                dt.datetime.now(dt.timezone.utc),
                f"{idx} activities downloaded so far.",
                error=False,
                complete=False,
            )

        i += 1

    print(f"All {i} activities downloaded.")
    save_download_status_to_dynamo(
        download_status_table,
        athlete_id,
        dt.datetime.now(dt.timezone.utc),
        f"All {i} activities downloaded.",
        error=False,
        complete=False,
    )
    save_summary_activities_to_s3(s3_client, athlete_id, summary_activities)
    print(f"All {i} activities saved to s3.")
    save_download_status_to_dynamo(
        download_status_table,
        athlete_id,
        dt.datetime.now(dt.timezone.utc),
        f"All {i} activities saved to s3.",
        error=False,
        complete=True,
    )


@app.get("/api/test_2")
async def test_2(request: Request) -> None:
    raise Exception("This is for testing sentry later ;)")
