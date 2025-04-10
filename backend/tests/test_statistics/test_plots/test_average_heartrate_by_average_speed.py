import pytest

from backend.exceptions import UserVisibleError
from backend.statistics.plots.average_heartrate_by_average_speed import plot
from tests.factories.activity_factories import ActivityFactory


def test_average_heartrate_by_average_speed_plot(some_basic_runs_and_rides) -> None:
    plot(some_basic_runs_and_rides)


def test_no_data(no_activities_at_all) -> None:
    with pytest.raises(UserVisibleError):
        plot(no_activities_at_all)


def test_average_heartrate_by_average_speed_few_activities() -> None:
    activities = [ActivityFactory(), ActivityFactory()]
    plot(_ for _ in activities)


def test_averate_heartrate_by_average_speed_real_data(real_activities) -> None:
    plot(real_activities)
