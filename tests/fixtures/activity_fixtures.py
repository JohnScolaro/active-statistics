import pytest
from stravalib.model import Activity

from tests.factories.activity_factories import ActivityFactory
from tests.factories.athlete_factories import AthleteFactory
from tests.factories.best_effort_factories import BestEffortFactory
from tests.factories.segment_factories import SegmentEffortFactory


@pytest.fixture
def some_basic_runs_and_rides() -> list[Activity]:
    athlete = AthleteFactory()
    return [
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
    ]


@pytest.fixture
def some_basic_runs_and_rides_without_heartrate() -> list[Activity]:
    athlete = AthleteFactory()
    return [
        ActivityFactory(
            athlete=athlete, type="Run", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Run", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Run", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Ride", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Ride", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Ride", average_heartrate=None, flagged=False
        ),
    ]


@pytest.fixture
def no_activities_at_all() -> list[Activity]:
    """
    A list containing zero activities.
    What if a Strava athlete who has never used Strava before in their life wants to use my website?
    Wouldn't that be wild?
    """
    return []


@pytest.fixture
def some_runs_with_best_efforts() -> list[Activity]:
    athlete = AthleteFactory()

    return [
        ActivityFactory(
            athlete=athlete,
            type="Run",
            best_efforts=[BestEffortFactory() for _ in range(5)],
            flagged=False,
        )
        for _ in range(5)
    ]


@pytest.fixture
def some_runs_with_segment_efforts() -> list[Activity]:
    """
    A fixture where each activity gets 5 segment efforts.
    """
    athlete = AthleteFactory()

    return [
        ActivityFactory(
            athlete=athlete,
            type="Run",
            segment_efforts=[SegmentEffortFactory() for _ in range(5)],
        )
        for _ in range(5)
    ]
