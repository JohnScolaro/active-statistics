from typing import Optional

import stravalib.unit_helper as uh
from stravalib.model import ActivityType, DetailedActivity

from backend.statistics.trivia import TriviaProcessor, TriviaTidbitBase


class MinAttributeTidbit(TriviaTidbitBase):
    """
    A type of tidbit that can calculate the min of any attribute for any activity type.
    """

    def __init__(self, activity_type: ActivityType, attribute_name: str) -> None:
        self.all_distances_zero: bool = True

        self.min_activity_id: Optional[int] = None
        self.attribute_name = attribute_name
        self.min_attribute_value: Optional[uh._Quantity] = None
        self.activity_type: Optional[ActivityType] = activity_type

    def reset_tidbit(self) -> None:
        self.all_distances_zero = True
        self.min_activity_id = None
        self.min_attribute_value = None

    def process_activity(self, activity: DetailedActivity) -> None:
        attr_value = getattr(activity, self.attribute_name)

        # If activity type is not correct, just return.
        if activity.type.root != self.activity_type:
            return

        # If the distance is non-zero and non-null, then turn off the "all distances null" flag.
        if attr_value is not None:
            if attr_value != 0.0:
                self.all_distances_zero = False

        if self.min_attribute_value is None or attr_value < self.min_attribute_value:
            self.min_attribute_value = attr_value
            self.min_activity_id = activity.id

    def get_description(self) -> str:
        return f"{self.activity_type} with Minimum {self.attribute_name.replace('_', ' ').title()}"

    def get_tidbit(self) -> Optional[str]:
        # If all the values have been zero, then chances are this is an
        # activity type that doesn't use distance like "workout". Just return
        # None in this case.
        if self.all_distances_zero:
            return None

        quantity = self.min_attribute_value
        if quantity is None:
            return None
        else:
            # Round the magnitude to nearest meter
            return f"{int(quantity)} meters"

    def get_activity_id(self) -> Optional[int]:
        return self.min_activity_id


class MaxAttributeTidbit(TriviaTidbitBase):
    """
    A type of tidbit that can calculate the min of any attribute for any activity type.
    """

    def __init__(self, activity_type: ActivityType, attribute_name: str) -> None:
        self.all_distances_zero: bool = True

        self.max_activity_id: Optional[int] = None
        self.attribute_name = attribute_name
        self.max_attribute_value: Optional[uh._Quantity] = None
        self.activity_type: Optional[ActivityType] = activity_type

    def reset_tidbit(self) -> None:
        self.all_distances_zero = True
        self.max_activity_id = None
        self.max_attribute_value = None

    def process_activity(self, activity: DetailedActivity) -> None:
        attr_value = getattr(activity, self.attribute_name)

        # If activity type is not the specified type, just return.
        if activity_type is not None:
            if activity.type.root != self.activity_type:
                return

        # If the distance is non-zero and non-null, then turn off the "all distances
        # null" flag.
        if attr_value is not None:
            if attr_value != 0.0:
                self.all_distances_zero = False

        if self.max_attribute_value is None or attr_value > self.max_attribute_value:
            self.max_attribute_value = attr_value
            self.max_activity_id = activity.id

    def get_description(self) -> str:
        return f"{self.activity_type} with Maximum {self.attribute_name.replace('_', ' ').title()}"

    def get_tidbit(self) -> Optional[str]:
        # If all the values have been zero, then chances are this is an
        # activity type that doesn't use distance like "workout". Just return
        # None in this case.
        if self.all_distances_zero:
            return None

        quantity = self.max_attribute_value
        if quantity is None:
            return None
        else:
            # Round the magnitude to nearest meter
            return f"{int(quantity)} meters"

    def get_activity_id(self) -> Optional[int]:
        return self.max_activity_id


min_and_max_distance_trivia_processor = TriviaProcessor()
min_and_max_elevation_trivia_processor = TriviaProcessor()
general_trivia = TriviaProcessor()

for activity_type in [
    "AlpineSki",
    "BackcountrySki",
    "Canoeing",
    "Crossfit",
    "EBikeRide",
    "Elliptical",
    "Golf",
    "Handcycle",
    "Hike",
    "IceSkate",
    "InlineSkate",
    "Kayaking",
    "Kitesurf",
    "NordicSki",
    "Ride",
    "RockClimbing",
    "RollerSki",
    "Rowing",
    "Run",
    "Sail",
    "Skateboard",
    "Snowboard",
    "Snowshoe",
    "Soccer",
    "StairStepper",
    "StandUpPaddling",
    "Surfing",
    "Swim",
    "Velomobile",
    "VirtualRide",
    "VirtualRun",
    "Walk",
    "WeightTraining",
    "Wheelchair",
    "Windsurf",
    "Workout",
    "Yoga",
]:
    min_and_max_distance_trivia_processor.register_tidbit(
        MinAttributeTidbit(activity_type, "distance")
    )
    min_and_max_distance_trivia_processor.register_tidbit(
        MaxAttributeTidbit(activity_type, "distance")
    )
    min_and_max_elevation_trivia_processor.register_tidbit(
        MinAttributeTidbit(activity_type, "total_elevation_gain")
    )
    min_and_max_elevation_trivia_processor.register_tidbit(
        MaxAttributeTidbit(activity_type, "total_elevation_gain")
    )
