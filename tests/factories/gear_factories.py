from typing import Optional

import factory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyFloat, FuzzyInteger
from stravalib.model import Gear


class GearFactory(factory.Factory):
    class Meta:
        model = Gear

    brand_name: Optional[str] = Faker("word")
    description: Optional[str] = Faker("word")
    frame_type: Optional[int] = FuzzyInteger(1, 100)
    model_name: Optional[str] = Faker("word")
    distance: Optional[float] = FuzzyFloat(0, 100_000)
    id: Optional[str] = FuzzyInteger(1, 1_000_000)
    name: Optional[str] = Faker("word")
    primary: Optional[bool] = FuzzyChoice([True, False])
    resource_state: Optional[int] = None
