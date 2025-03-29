import datetime as dt
import random

import factory
from factory import LazyAttribute
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyFloat, FuzzyInteger
from faker import Faker
from stravalib.model import SummaryActivity
from stravalib.unit_helper import _Quantity

from tests.factories.athlete_factories import MetaAthleteFactory

fake = Faker()


class ActivityFactory(factory.Factory):
    class Meta:
        model = SummaryActivity

    id = FuzzyInteger(1, 999_999_999)
    achievement_count = FuzzyInteger(0, 100)
    athlete = MetaAthleteFactory()
    athlete_count = FuzzyInteger(1, 10)
    average_speed = LazyAttribute(lambda _: _Quantity(random.uniform(1, 10)))
    average_heartrate = FuzzyFloat(80, 210)
    average_watts = FuzzyInteger(1, 200)
    comment_count = FuzzyInteger(0, 10)
    commute = FuzzyChoice([True, False])
    device_watts = False
    distance = FuzzyFloat(1, 10_000)
    elapsed_time = FuzzyInteger(60, 2 * 60 * 60)
    elev_high = FuzzyFloat(100, 200)
    elev_low = FuzzyFloat(0, 100)
    end_latlng = LazyAttribute(
        lambda _: (float(fake.latitude()), float(fake.longitude()))
    )
    external_id = LazyAttribute(lambda _: str(FuzzyInteger(1, 999_999)))
    flagged = FuzzyChoice([True, False])
    gear_id = None
    gear = None
    has_kudoed = None
    hide_from_home = None
    kilojoules = None
    kudos_count = None
    manual = None
    map = None
    max_speed = FuzzyFloat(1, 20)
    max_watts = FuzzyInteger(1, 200)
    moving_time = FuzzyInteger(60, 2 * 60 * 60)
    name = LazyAttribute(lambda _: fake.text(max_nb_chars=30))
    photo_count = FuzzyInteger(0, 10)
    private = FuzzyChoice([True, False])
    sport_type = LazyAttribute(lambda obj: obj.type)
    start_date = FuzzyDateTime(
        dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc),
        dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc),
    )
    start_date_local = FuzzyDateTime(
        dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc),
        dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc),
    )
    start_latlng = LazyAttribute(
        lambda _: (float(fake.latitude()), float(fake.longitude()))
    )
    timezone = None
    total_elevation_gain = FuzzyFloat(0, 2000)
    total_photo_count = FuzzyInteger(0, 3)
    trainer = None
    type = FuzzyChoice(["Run", "Ride"])
    upload_id = None
    upload_id_str = None
    weighted_average_watts = None
    workout_type = None


class DetailedActivityFactory(ActivityFactory):
    pass
