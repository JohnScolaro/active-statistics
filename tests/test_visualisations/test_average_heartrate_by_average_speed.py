import pytest

from active_statistics.exceptions import UserVisibleException
from active_statistics.statistics.plots.average_heartrate_by_average_speed import plot


def test_average_heartrate_by_average_speed_animation(
    some_basic_runs_and_rides,
) -> None:
    plot(some_basic_runs_and_rides)


def test_no_data(no_activities_at_all) -> None:
    with pytest.raises(UserVisibleException):
        plot(no_activities_at_all)
