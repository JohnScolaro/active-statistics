import datetime as dt
from typing import Literal, Optional

import factory
from factory import LazyAttribute
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyFloat, FuzzyInteger
from stravalib.model import (
    Activity,
    Athlete,
    AthletePrEffort,
    AthleteSegmentStats,
    LatLng,
    Map,
    PolylineMap,
    Segment,
    SegmentEffort,
    SegmentEffortAchievement,
)
from tests.factories.activity_factories import ActivityFactory
from tests.factories.athlete_factories import AthleteFactory


class SegmentFactory(factory.Factory):
    class Meta:
        model = Segment

    map: Optional[Map] = None
    athlete_segment_stats: Optional[AthleteSegmentStats] = None
    athlete_pr_effort: Optional[AthletePrEffort] = None
    activity_type: Optional[Literal["Ride", "Run"]] = FuzzyChoice(["Run", "Ride"])

    start_latitude: Optional[float] = None
    end_latitude: Optional[float] = None
    start_longitude: Optional[float] = None
    end_longitude: Optional[float] = None
    starred: Optional[bool] = None
    pr_time: Optional[int] = None
    starred_date: Optional[dt.datetime] = None
    elevation_profile: Optional[str] = None

    athlete_count: Optional[int] = None
    created_at: Optional[dt.datetime] = None
    effort_count: Optional[int] = None
    hazardous: Optional[bool] = None
    star_count: Optional[int] = None
    total_elevation_gain: Optional[float] = None
    updated_at: Optional[dt.datetime] = None

    average_grade: Optional[float] = None
    city: Optional[str] = None
    climb_category: Optional[int] = None
    country: Optional[str] = None
    distance: Optional[float] = None
    elevation_high: Optional[float] = None
    elevation_low: Optional[float] = None
    end_latlng: Optional[LatLng] = None
    id: Optional[int] = FuzzyInteger(1, 999_999)
    maximum_grade: Optional[float] = None
    name: Optional[str] = Faker("name")
    private: Optional[bool] = None
    start_latlng: Optional[LatLng] = None
    state: Optional[str] = None


class SegmentEffortFactory(factory.Factory):
    class Meta:
        model = SegmentEffort

    achievements: Optional[list[SegmentEffortAchievement]] = None
    segment: Optional[Segment] = LazyAttribute(lambda _: SegmentFactory())
    activity: Optional[Activity] = LazyAttribute(lambda _: ActivityFactory())
    athlete: Optional[Athlete] = LazyAttribute(lambda _: AthleteFactory())
    average_cadence: Optional[float] = FuzzyFloat(80, 200)
    average_heartrate: Optional[float] = FuzzyFloat(60, 180)
    average_watts: Optional[float] = FuzzyFloat(50, 400)
    device_watts: Optional[bool] = FuzzyChoice([True, False])
    kom_rank: Optional[int] = FuzzyChoice(list(i + 1 for i in range(10)) + [None])
    max_heartrate: Optional[float] = FuzzyFloat(150, 210)
    moving_time: Optional[int] = FuzzyFloat(60 * 2, 2 * 60 * 60)
    name: Optional[str] = Faker("name")
    pr_rank: Optional[int] = FuzzyChoice(list(i + 1 for i in range(3)) + [None])


class SegmentEffortAchievementFactory(factory.Factory):
    class Meta:
        model = SegmentEffortAchievement

    rank = FuzzyInteger(1, 10)
    type = FuzzyChoice(["year_pr", "overall"])
    type_id = FuzzyInteger(0, 10)
    effort_count = FuzzyInteger(1, 100)
