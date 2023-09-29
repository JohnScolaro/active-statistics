import datetime as dt
import json
import logging
import time
from typing import Iterator, Optional, Type

import plotly.graph_objects as go
import sentry_sdk
from plotly.utils import PlotlyJSONEncoder
from rq.job import Job, get_current_job
from stravalib.client import Client
from stravalib.exc import RateLimitExceeded
from stravalib.model import Activity
from stravalib.protocol import AccessInfo
from stravalib.strava_model import SummaryActivity
from stravalib.util.limiter import RateLimiter

from active_statistics.gui.gui import all_tabs
from active_statistics.gui.plot_tabs import PlotTab
from active_statistics.gui.trivia_tabs import TableTab
from active_statistics.logging import TASK, setup_task_logging
from active_statistics.strava_custom_rate_limiters import DetailedTaskRateLimiter
from active_statistics.utils import redis
from active_statistics.utils.environment_variables import evm
from active_statistics.utils.local_storage import (
    delete_athlete_storage_location,
    get_activity_iterator,
    get_summary_activity_iterator,
    save_activity_to_file,
    save_summary_activities_to_file,
)
from active_statistics.utils.s3 import save_plot_data

setup_task_logging()

logger: logging.Logger = logging.getLogger(TASK)


def get_and_process_summary_statistics(athlete_id: int) -> None:
    log(logger.info, f"Getting Summary Statistics for {athlete_id}")

    client = get_client_for_athlete(athlete_id)

    summary_activities: list[SummaryActivity] = get_summary_activities(
        client, athlete_id
    )
    save_summary_activities_to_file(athlete_id, summary_activities)

    if evm.use_s3():
        process_activities(athlete_id, detailed=False)
        delete_athlete_storage_location(athlete_id)


def get_and_process_detailed_statistics(athlete_id: int) -> None:
    log(logger.info, f"Getting Detailed Statistics for {athlete_id}")

    client = get_client_for_athlete(athlete_id, rate_limiter=DetailedTaskRateLimiter())

    summary_activities: list[SummaryActivity] = get_summary_activities(
        client, athlete_id
    )

    get_and_save_detailed_activities(
        client, athlete_id, list(activity.id for activity in summary_activities)
    )
    if evm.use_s3():
        process_activities(athlete_id, detailed=True)
        delete_athlete_storage_location(athlete_id)


def get_and_save_detailed_activities(
    client: Client, athlete_id: int, activity_ids: list[int]
) -> None:
    activity_num = 0
    while activity_num < len(activity_ids):
        try:
            # Although unnecessary, by assigning this it's own variable, it
            # should let Sentry record the specific event ID that breaks the
            # app instead of returning the truncated list of all ID's.
            activity_id_to_get = activity_ids[activity_num]

            detailed_activity = client.get_activity(
                activity_id_to_get, include_all_efforts=True
            )
            log(logger.info, f"Saving detailed data for activity {activity_num + 1}.")
            save_activity_to_file(athlete_id, detailed_activity)
            activity_num += 1
        except RateLimitExceeded as e:
            seconds_to_sleep = int(e.timeout) + 1
            log(
                logger.info,
                f"Got rate limited. Sleeping for {e.timeout} seconds.",
            )
            for i in range(seconds_to_sleep):
                log(
                    logger.debug,
                    f"Got rate limited. Sleeping for {seconds_to_sleep - i} seconds.",
                )
                time.sleep(1)


def get_client_for_athlete(
    athlete_id: int, rate_limiter: Optional[Type[RateLimiter]] = None
) -> Client:
    """
    Given an athlete id, return a client with the key so

    Returns:
    * Client
    * None if something went wrong.
    """
    expires_at = redis.get_strava_api_access_token_expires_at(athlete_id)
    if expires_at is None:
        # Shouldn't be able to get here, but one way that you can, is if mid-data-download, I flush all redis dbs.
        # In that case, the user should be logged out.
        # That's a TODO though, and for now just treat this as impossible.
        log(
            logger.error,
            "Don't know when token expires for user who is requesting data.",
        )
        raise Exception(
            "Don't know when token expires for user who is requesting data."
        )

    # If the access key is going to expire within 30 minutes of getting this key, get another fresh one.
    # We don't want our key expiring mid-download.
    if dt.datetime.now() >= expires_at - dt.timedelta(minutes=30):
        client = Client(rate_limiter=rate_limiter)
        access_info: AccessInfo = client.refresh_access_token(
            client_id=evm.get_strava_client_id(),
            client_secret=evm.get_strava_client_secret(),
            refresh_token=redis.get_strava_api_refresh_token(athlete_id),
        )
        redis.set_strava_access_tokens(athlete_id, access_info)

    access_token = redis.get_strava_api_access_token(athlete_id)
    if access_token is None:
        # Also shouldn't ever get here. I think I'd have to wipe the db as code
        # execution is between this call, and where I get the expiry time above.
        log(logger.error, "Don't have access token for user who is requesting data.")
        raise Exception("Don't have access token for user who is requesting data.")

    # Set the clients access token for the user.
    client = Client(access_token=access_token, rate_limiter=rate_limiter)
    return client


def get_summary_activities(client: Client, athlete_id: int) -> list[SummaryActivity]:
    """
    Gets all the summary activities and adds some logging around it.
    """
    log(logger.info, f"Getting summary activities for athlete: {athlete_id}")
    summary_activities: list[SummaryActivity] = list(client.get_activities())
    log(
        logger.info,
        f"Recieved {len(summary_activities)} activities for athlete: {athlete_id}",
    )
    return summary_activities


def process_activities(athlete_id: int, detailed: bool) -> None:
    """
    Process activities is a pretty vague name. This function takes a list of
    either summary or detailed activities and then loops over all the pages in
    the website, and calls the plot function of tabs that use either summary or
    detailed activities to make plots. This gives us a bunch of data. This data
    is then saved to s3.
    """
    for tab in all_tabs:
        if tab.is_detailed() == detailed:
            try:
                activity_iterator: Iterator[Activity] = (
                    get_activity_iterator(athlete_id)
                    if detailed
                    else get_summary_activity_iterator(athlete_id)
                )

                log(
                    logger.info,
                    f'Processing {"detailed " if detailed else ""}data for: "{tab.get_name()}" tab.',
                )
                if isinstance(tab, PlotTab):
                    fig: go.Figure = tab.plot_function(activity_iterator)
                    json_data = json.dumps(fig, cls=PlotlyJSONEncoder)
                if isinstance(tab, TableTab):
                    data = tab.get_table_data(activity_iterator)
                    json_data = json.dumps(data, cls=PlotlyJSONEncoder)

                save_plot_data(athlete_id, tab.get_key(), json_data)

            except Exception as e:
                # If we get an exception in the data generation, just throw it into Sentry, but soldier on.
                log(
                    logger.exception,
                    f"An exception happened while generating plot data. Here it is: {e}",
                )
                sentry_sdk.capture_exception(e)


def log(log_fuction, message: str) -> None:
    """
    We want to log messages from tasks in two ways:
        1: Save to file.
        2: Save into job arbitrary memory, so we can give it to the 'request
            data status' requests as something useful to show the user.
    """
    log_fuction(message)
    job = get_current_job()
    if isinstance(job, Job):
        job.meta["message"] = message
        job.save()
