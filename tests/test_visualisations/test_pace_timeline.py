import datetime as dt

import pytest
from stravalib.unithelper import Quantity

from active_statistics.exceptions import UserVisibleException
from active_statistics.statistics.plots.pace_timeline import plot
from tests.factories.activity_factories import ActivityFactory


def test_pace_timeline(some_basic_runs_and_rides) -> None:
    plot(some_basic_runs_and_rides)


def test_no_data(no_activities_at_all) -> None:
    with pytest.raises(UserVisibleException):
        plot(no_activities_at_all)


def test_first_activities_have_no_average_speeds() -> None:
    activities = [
        ActivityFactory(
            type="Run",
            start_date_local=dt.datetime(2015, 1, 1, 6),
            average_speed=Quantity(0.0, "m/s"),
            moving_time=0,
        ),
        ActivityFactory(
            type="Run",
            start_date_local=dt.datetime(2020, 1, 1, 6),
            average_speed=Quantity(10, "m/s"),
        ),
    ]
    plot(_ for _ in activities)
