import datetime as dt

import factory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyFloat, FuzzyInteger
from stravalib.model import MetaAthlete, SummaryAthlete


class MetaAthleteFactory(factory.Factory):
    class Meta:
        model = MetaAthlete

    id: int = FuzzyInteger(1, 999_999)


class AthleteFactory(factory.Factory):
    class Meta:
        model = SummaryAthlete

    id: int = FuzzyInteger(1, 999_999)
    resource_state = None
    firstname = Faker("first_name")
    lastname = Faker("last_name")
    profile_medium = None
    profile = None
    city = Faker("city")
    state = None
    country = Faker("country")
    sex = FuzzyChoice(["M", "F"])
    premium = FuzzyChoice([True, False])
    summit = None
    created_at = FuzzyDateTime(
        dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc),
        dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc),
    )
    updated_at = FuzzyDateTime(
        dt.datetime(2022, 1, 1, tzinfo=dt.timezone.utc),
        dt.datetime(2023, 1, 1, tzinfo=dt.timezone.utc),
    )
    follower_count = FuzzyInteger(0, 100)
    friend_count = FuzzyInteger(0, 100)
    measurement_preference = "meters"
    ftp = FuzzyFloat(1, 200)
    weight = FuzzyInteger(50, 200)
    clubs = None
    bikes = None
    shoes = None
