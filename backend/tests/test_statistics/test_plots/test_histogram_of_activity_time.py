import pytest

from backend.exceptions import UserVisibleError
from backend.statistics.plots.histogram_of_activity_time import plot


def test_histogram_of_activity_time(some_basic_runs_and_rides) -> None:
    plot(some_basic_runs_and_rides)


def test_no_data(no_activities_at_all) -> None:
    with pytest.raises(UserVisibleError):
        plot(no_activities_at_all)
