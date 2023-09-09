import pytest

from active_statistics.exceptions import UserVisibleException
from active_statistics.statistics.plots.pace_timeline import plot


def test_pace_timeline(some_basic_runs_and_rides) -> None:
    plot(some_basic_runs_and_rides)


def test_no_data(no_activities_at_all) -> None:
    with pytest.raises(UserVisibleException):
        plot(no_activities_at_all)
