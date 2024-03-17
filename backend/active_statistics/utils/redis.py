"""
This file will house all the code that interacts with redis.
"""

import datetime as dt
from typing import Optional

import redis
from active_statistics.constants import DATA_TIMEOUT
from stravalib.protocol import AccessInfo

# A DB to store Strava API access tokens.
r_api_access = redis.Redis(host="localhost", port=6379, db=0)

# A DB to hold a the rq task queue
r_task_queue = redis.Redis(host="localhost", port=6379, db=1)

# DBs to hold the last times that users hit refresh.
r_last_summary_refresh = redis.Redis(host="localhost", port=6379, db=2)
r_last_detailed_refresh = redis.Redis(host="localhost", port=6379, db=3)


def set_strava_access_tokens(athlete_id: int, access_keys: AccessInfo) -> None:
    r_api_access.set(
        str(athlete_id),
        ",".join(
            [
                access_keys["access_token"],
                access_keys["refresh_token"],
                str(access_keys["expires_at"]),
            ]
        ),
    )


def get_strava_api_access_token(athlete_id: int) -> Optional[str]:
    bytes = r_api_access.get(str(athlete_id))
    if bytes is None:
        return None
    value = bytes.decode("utf8")
    return value.split(",")[0]


def get_strava_api_refresh_token(athlete_id: int) -> Optional[str]:
    bytes = r_api_access.get(str(athlete_id))
    if bytes is None:
        return None
    value = bytes.decode("utf8")
    return value.split(",")[1]


def get_strava_api_access_token_expires_at(athlete_id: int) -> Optional[dt.datetime]:
    bytes = r_api_access.get(str(athlete_id))
    if bytes is None:
        return None
    value = bytes.decode("utf8")
    return dt.datetime.fromtimestamp(int(value.split(",")[2]))


def delete_strava_api_access_tokens(athlete_id: int) -> None:
    r_api_access.delete(str(athlete_id))


def get_last_detailed_refresh_time(athlete_id: int) -> Optional[dt.datetime]:
    """
    Get the last time that a user refreshed their data. If None is returned, then there is no record of the user having refreshed their data.
    """
    last_time_raw: Optional[bytes] = r_last_detailed_refresh.get(str(athlete_id))
    if last_time_raw is None:
        return None
    else:
        return dt.datetime.fromisoformat(last_time_raw.decode())


def set_last_detailed_refresh_time(athlete_id: int) -> None:
    """
    Set the last refresh time in the database to be now.
    """
    r_last_detailed_refresh.set(str(athlete_id), dt.datetime.now().isoformat())
    r_last_detailed_refresh.expire(str(athlete_id), DATA_TIMEOUT)


def get_last_summary_refresh_time(athlete_id: int) -> Optional[dt.datetime]:
    """
    Get the last time that a user refreshed their data. If None is returned, then there is no record of the user having refreshed their data.
    """
    last_time_raw: Optional[bytes] = r_last_summary_refresh.get(str(athlete_id))
    if last_time_raw is None:
        return None
    else:
        return dt.datetime.fromisoformat(last_time_raw.decode())


def set_last_summary_refresh_time(athlete_id: int) -> None:
    """
    Set the last refresh time in the database to be now.
    """
    r_last_summary_refresh.set(str(athlete_id), dt.datetime.now().isoformat())
    r_last_summary_refresh.expire(str(athlete_id), DATA_TIMEOUT)
