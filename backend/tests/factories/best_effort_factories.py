import datetime as dt
from typing import Optional

import factory
from factory import LazyAttribute
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyFloat, FuzzyInteger
from stravalib.model import Activity, Athlete, BestEffort, Segment

# A few options for the best effort lengths
BEST_EFFORT_LENGTHS = [
    "400m",
    "1/2 mile",
    "1k",
    "1 mile",
    "2 mile",
    "5k",
    "10k",
    "15k",
    "10 mile",
    "20k",
    "Half-Marathon",
]


class BestEffortFactory(factory.Factory):
    class Meta:
        model = BestEffort

    # Best efforts aren't segments so this is always None.
    segment: Optional[Segment] = None

    activity: Optional[Activity] = None
    athlete: Optional[Athlete] = None
    average_cadence: Optional[float] = FuzzyFloat(60, 180)
    average_heartrate: Optional[float] = FuzzyFloat(80, 160)
    average_watts: Optional[float] = None
    device_watts: Optional[bool] = None
    end_index: Optional[int] = FuzzyInteger(1, 1_000)
    hidden: Optional[bool] = None
    kom_rank: Optional[int] = FuzzyChoice([None] + list(i + 1 for i in range(10)))
    max_heartrate: Optional[float] = LazyAttribute(lambda x: x.average_heartrate + 20)
    moving_time: Optional[int] = FuzzyInteger(5 * 60, 2 * 60 * 60)
    name: Optional[str] = FuzzyChoice(BEST_EFFORT_LENGTHS)
    pr_rank: Optional[int] = FuzzyChoice([None] + list(i + 1 for i in range(3)))
    start_index: Optional[int] = None

    activity_id: Optional[int] = FuzzyInteger(1, 999_999)
    distance: Optional[float] = FuzzyFloat(1, 10_000)
    elapsed_time: Optional[int] = FuzzyInteger(60, 2 * 60 * 60)
    id: Optional[int] = FuzzyInteger(1, 999_999)
    is_kom: Optional[bool] = FuzzyChoice([True, False])
    start_date: Optional[dt.datetime] = FuzzyDateTime(
        dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc),
        dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc),
    )
    start_date_local: Optional[dt.datetime] = LazyAttribute(lambda x: x.start_date)
