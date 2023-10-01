import datetime as dt

from active_statistics.statistics.trivia import TriviaProcessor
from active_statistics.statistics.trivia.summary_trivia import (
    MostConsecutiveDaysOfActivities,
)
from tests.factories.activity_factories import ActivityFactory


def test_general_trivia(some_basic_runs_and_rides) -> None:
    """
    Tests that the most consecutive days calculator is correct.
    """
    processor = TriviaProcessor()
    processor.register_tidbit(MostConsecutiveDaysOfActivities())

    activities = [
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 1, 2)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 2, 19)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 4, 3)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 5, 10)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 6, 1)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 7, 22)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 7, 23)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 10, 1)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 10, 2)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 10, 3)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 11, 4)),
        ActivityFactory(start_date_local=dt.datetime(2023, 1, 12, 5)),
    ]

    result = processor.get_data(activity for activity in activities)
    assert result[0][1] == "4 days (2023-01-04 to 2023-01-07)"
