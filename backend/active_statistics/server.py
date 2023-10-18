import dataclasses
import datetime as dt
import json
import logging
import os
from typing import Any, Optional

from active_statistics.app_logging import SERVER, setup_server_logging
from active_statistics.communication_schema import (
    DataStatusMessage,
    RefreshStatusMessage,
)
from active_statistics.gui.gui import all_tabs
from active_statistics.gui.tab_group import TabGroup
from active_statistics.gui.tabs import Tab
from active_statistics.utils import human_readable_time, redis, rq
from active_statistics.utils.environment_variables import evm
from active_statistics.utils.local_storage import (
    delete_detailed_activities,
    delete_summary_activities,
    we_have_detailed_activities_for_athlete,
    we_have_summary_activities_for_athlete,
)
from active_statistics.utils.sentry import set_up_sentry_for_server
from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from requests.exceptions import HTTPError
from rq.job import JobStatus
from stravalib.client import Client
from stravalib.exc import RateLimitExceeded
from stravalib.model import Athlete
from werkzeug.wrappers import Response

setup_server_logging()
logger = logging.getLogger(SERVER)

if evm.is_production():
    set_up_sentry_for_server()

app = Flask(__name__)
app.secret_key = evm.get_flask_secret_key()


def get_strava_auth_url() -> str:
    logger.info("getting auth url")
    scheme = "https" if evm.is_production() else "http"
    redirect_uri = (
        f"{scheme}://{evm.get_domain()}:{str(evm.get_port())}/api/authenticate"
    )

    client = Client()
    authorize_url: str = client.authorization_url(
        client_id=evm.get_strava_client_id(), redirect_uri=redirect_uri
    )
    return authorize_url


@app.route("/api/example_chart_data")
def chart_data() -> Response:
    current_file_dir_path = os.path.dirname(os.path.realpath(__file__))
    example_chart_data_path = os.path.join(
        current_file_dir_path, "static", "example_charts", "personal_bests.json"
    )
    # Read the example file
    with open(example_chart_data_path, "r") as f:
        json_data = f.read()

    chart_json = json.loads(json_data)
    return make_response(jsonify(chart_json))


@app.route("/api/authenticate")
def authenticate() -> Response:
    # Retrieve query parameters
    code: str = request.args["code"]
    scope: str = request.args["scope"]

    # Do some terrible scope checking.
    # If we aren't given permission to read activities, just return to index.
    if scope != "read,activity:read":
        return redirect(url_for("index", scope_incorrect=True))

    # Try the following. It can fail in a couple different ways, all due to
    # hitting the Strava rate limit.
    try:
        client = Client()
        token_response = client.exchange_code_for_token(
            client_id=evm.get_strava_client_id(),
            client_secret=evm.get_strava_client_secret(),
            code=code,
        )
        client.access_token = token_response["access_token"]

        athlete: Athlete = client.get_athlete()
        redis.set_strava_access_tokens(athlete.id, token_response)
        session["athlete_id"] = athlete.id
    except (HTTPError, RateLimitExceeded) as e:
        return redirect(url_for("index", rate_limit_exceeded=True))

    response = make_response(redirect("/home"))
    response.set_cookie("logged_in", "true")
    return response


@app.route("/api/refresh_summary_data")
def refresh_summary_data() -> Response:
    """
    When this endpoint is hit, we will endevour to re-download the users summary data, assuming they haven't already
    refreshed in the last day.
    """
    if "athlete_id" not in session:
        return redirect(url_for("index"))

    athlete_id = int(session["athlete_id"])
    summary_refresh_min_period = dt.timedelta(days=1)

    # Check redis to see if they've refreshed recently.
    last_refresh_time = redis.get_last_summary_refresh_time(athlete_id)
    if last_refresh_time is None:
        # If there isn't a record of them reading data, put it on the queue.
        redis.set_last_summary_refresh_time(athlete_id)
        if not evm.use_s3():
            delete_summary_activities(athlete_id)
        rq.enqueue_summary_task(athlete_id)
        return make_response(
            jsonify(
                RefreshStatusMessage(
                    message="Adding refresh request to the queue", refresh_accepted=True
                )
            )
        )

    time_since_last_refresh = dt.datetime.now() - last_refresh_time
    if time_since_last_refresh >= summary_refresh_min_period:
        # If they last refreshed over a day ago, put it in the queue.
        redis.set_last_summary_refresh_time(athlete_id)
        if not evm.use_s3():
            delete_summary_activities(athlete_id)
        rq.enqueue_summary_task(athlete_id)
        return make_response(
            jsonify(
                RefreshStatusMessage(
                    message="Adding refresh request to the queue", refresh_accepted=True
                )
            )
        )

    # Otherwise, just return a message saying they've requested too recently.
    return make_response(
        jsonify(
            RefreshStatusMessage(
                message=f"You have refreshed too recently. Please wait {human_readable_time.timedelta_to_human_readable_string(summary_refresh_min_period - time_since_last_refresh)} until refreshing again.",
                refresh_accepted=False,
            )
        )
    )


@app.route("/api/refresh_detailed_data")
def refresh_detailed_data() -> Response:
    """
    When this endpoint is hit, we will endevour to re-download the users detailed activity data, assuming they haven't
    already refreshed in the last day.
    """
    if "athlete_id" not in session:
        return redirect(url_for("index"))

    athlete_id = int(session["athlete_id"])

    # In case anyone decides to be smart and just manually ping this endpoint
    # to get their detailed data without paying, check before refreshing the data:
    if evm.is_production():
        return make_response(
            jsonify(RefreshStatusMessage(message="Nice try.", refresh_accepted=False))
        )

    detailed_refresh_min_period = dt.timedelta(days=7)

    # Check redis to see if they've refreshed recently.
    last_refresh_time = redis.get_last_detailed_refresh_time(athlete_id)
    if last_refresh_time is None:
        # If there isn't a record of them reading data, put it on the queue.
        redis.set_last_detailed_refresh_time(athlete_id)
        if not evm.use_s3():
            delete_detailed_activities(athlete_id)
        rq.enqueue_detailed_task(athlete_id)
        return make_response(
            jsonify(
                RefreshStatusMessage(
                    message="Adding refresh request to the queue", refresh_accepted=True
                )
            )
        )

    time_since_last_refresh = dt.datetime.now() - last_refresh_time
    if time_since_last_refresh >= detailed_refresh_min_period:
        # If they last refreshed over a week ago, put it in the queue.
        redis.set_last_detailed_refresh_time(athlete_id)
        if not evm.use_s3():
            delete_detailed_activities(athlete_id)
        rq.enqueue_detailed_task(athlete_id)
        return make_response(
            jsonify(
                RefreshStatusMessage(
                    message=f"Adding refresh request to the queue",
                    refresh_accepted=True,
                )
            )
        )

    # Otherwise, just return a message saying they've requested too recently.
    return make_response(
        jsonify(
            RefreshStatusMessage(
                message=f"You have refreshed too recently. Please wait {human_readable_time.timedelta_to_human_readable_string(detailed_refresh_min_period - time_since_last_refresh)} until refreshing again.",
                refresh_accepted=False,
            )
        )
    )


@app.route("/api/summary_data_status")
def summary_data_status() -> Response:
    """
    An endpoint that is constantly polled by the webserver for the status of the data until
    it eventually returns that data has been downloaded.
    """

    if "athlete_id" not in session:
        return redirect(url_for("index"))

    athlete_id = int(session["athlete_id"])

    # Firstly, if we are running in local mode, just check if there is data locally.
    if not evm.use_s3():
        if we_have_summary_activities_for_athlete(athlete_id):
            return make_response(
                jsonify(
                    DataStatusMessage(
                        message="Found data locally.",
                        status=JobStatus.FINISHED,
                        stop_polling=True,
                    )
                )
            )

    # Check rq to see is there is a result from a previous job for this athlete.
    job_status: Optional[JobStatus] = rq.get_summary_task_job_status(athlete_id)
    if job_status == "queued":
        queue_position = rq.get_position_in_summary_queue(athlete_id)
        queued_message = (
            "queued"
            if queue_position is None
            else f"Position {queue_position} in the queue."
        )
        return make_response(
            jsonify(
                DataStatusMessage(
                    message=queued_message, status=job_status, stop_polling=False
                )
            )
        )
    elif job_status == "started":
        # If the job has started, return the live message.
        message = rq.get_summary_job_message(athlete_id) or "Task has Started"
        return make_response(
            jsonify(
                DataStatusMessage(
                    message=message, status=job_status, stop_polling=False
                )
            )
        )
    elif job_status == "canceled" or job_status == "failed":
        return make_response(
            jsonify(
                DataStatusMessage(
                    message="Oh no! Something went wrong! Chances are I already know about it, but feel free to email me at johnscolaro95@gmail.com.",
                    status=job_status,
                    stop_polling=True,
                )
            )
        )
    elif job_status == "finished":
        last_refresh_time = redis.get_last_summary_refresh_time(athlete_id)
        if last_refresh_time:
            message = f"Data last refreshed at: {human_readable_time.datetime_to_human_readable_string(last_refresh_time)}."
        else:
            message = "No record of summary data having been downloaded has been found."
        return make_response(
            jsonify(
                DataStatusMessage(
                    message=message,
                    status=job_status,
                    stop_polling=True,
                )
            )
        )
    elif job_status is None:
        return make_response(
            jsonify(
                DataStatusMessage(
                    message="No record of summary data having been downloaded has been found.",
                    status=job_status,
                    stop_polling=True,
                )
            )
        )
    else:
        return make_response(
            jsonify(
                DataStatusMessage(
                    message=str(job_status), status=job_status, stop_polling=True
                )
            )
        )
        # Shouldn't get here.


@app.route("/api/detailed_data_status")
def detailed_data_status() -> Response:
    """
    An endpoint that is constantly polled by the webserver for the status of the data until
    it eventually returns that data has been downloaded.
    """

    if "athlete_id" not in session:
        return redirect(url_for("index"))

    athlete_id = int(session["athlete_id"])

    # Firstly, if we are running in local mode, just check if there is data locally.
    if not evm.use_s3():
        if we_have_detailed_activities_for_athlete(athlete_id):
            return make_response(
                jsonify(
                    DataStatusMessage(
                        message="Found data locally.",
                        status=JobStatus.FINISHED,
                        stop_polling=True,
                    )
                )
            )

    # Check rq to see is there is a result from a previous job for this athlete.
    job_status: Optional[JobStatus] = rq.get_detailed_task_job_status(athlete_id)
    if job_status == "queued":
        queue_position = rq.get_position_in_detailed_queue(athlete_id)
        queued_message = (
            "queued"
            if queue_position is None
            else f"Position {queue_position} in the queue."
        )
        return make_response(
            jsonify(
                DataStatusMessage(
                    message=queued_message, status=job_status, stop_polling=False
                )
            )
        )
    elif job_status == "started":
        # If the job has started, return the live message.
        message = rq.get_detailed_job_message(athlete_id) or "Task has Started"
        return make_response(
            jsonify(
                DataStatusMessage(
                    message=message, status=job_status, stop_polling=False
                )
            )
        )
    elif job_status == "canceled" or job_status == "failed":
        return make_response(
            jsonify(
                DataStatusMessage(
                    message="Oh no! Something went wrong! Chances are I already know about it, but feel free to email me at johnscolaro95@gmail.com.",
                    status=job_status,
                    stop_polling=True,
                )
            )
        )
    elif job_status == "finished":
        last_refresh_time = redis.get_last_detailed_refresh_time(athlete_id)
        if last_refresh_time:
            message = f"Data last refreshed at: {human_readable_time.datetime_to_human_readable_string(last_refresh_time)}."
        else:
            message = "No record of summary data having been downloaded has been found."
        return make_response(
            jsonify(
                DataStatusMessage(
                    message=message,
                    status=job_status,
                    stop_polling=True,
                )
            )
        )
    elif job_status is None:
        return make_response(
            jsonify(
                DataStatusMessage(
                    message="No record of detailed data having been downloaded has been found.",
                    status=job_status,
                    stop_polling=True,
                )
            )
        )
    else:
        return make_response(
            jsonify(
                DataStatusMessage(
                    message=str(job_status), status=job_status, stop_polling=True
                )
            )
        )
        # Shouldn't get here.


@app.route("/api/download_data")
def download_data() -> Response:
    if "athlete_id" not in session:
        return redirect(url_for("index"))

    return make_response(
        render_template(
            "download_data_main_content_container.html",
            explanation="Welcome to Active Statistics! This tab is where you can refresh your plots with your latest data. There are two types of visualisation on this website. Visualisations that require 'detailed data' and visualisations that require summmary data. The summary and visualisation tabs are seperated on the left side with small horizontal lines. Summary data is automatically downloaded when you log in for the first time because it only takes a few seconds to download. If you wish to view visualisation that require detailed data, you'll have to manually click the 'refresh detailed data' button. Be prepared - this can take a while. It may take ~30 minutes if you have over 400 activities.",
        )
    )


@app.route("/api/logout")
def logout() -> Response:
    if "athlete_id" not in session:
        return redirect(url_for("index"))

    athlete_id = int(session["athlete_id"])

    redis.delete_strava_api_access_tokens(athlete_id)

    # Clear the user session
    session.clear()

    # Redirect to index to reconnect with strava.
    return redirect(url_for("index"))


@app.route("/api/paid")
def paid() -> Response:
    """
    Responds with whether this user is paid or not.
    """
    if "athlete_id" not in session:
        return redirect(url_for("index"))

    athlete_id = int(session["athlete_id"])

    # For now, nobody has paid. Unless you're running this locally, then you can have access to it.
    return make_response(jsonify({"paid": not evm.is_production()}))


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


@app.route("/api/tabs")
def tabs_route() -> Response:
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

    return make_response(jsonify(expand_tabs(all_tabs)))


# Before the app starts, we want to generate all the routes for our tabs.
for tab in all_tabs:

    def generate_and_register_routes_for_children(tab_group: TabGroup) -> None:
        for tab in tab_group.children:
            if isinstance(tab, Tab):
                tab.generate_and_register_routes(app, evm)
            if isinstance(tab, TabGroup):
                generate_and_register_routes_for_children(tab)

    if isinstance(tab, Tab):
        tab.generate_and_register_routes(app, evm)
    if isinstance(tab, TabGroup):
        generate_and_register_routes_for_children(tab)


if not evm.is_production():
    app.run(debug=True)
