from stravalib.model import Activity

from active_statistics.trivia.min_max_summary_trivia import (
    MaxAttributeTidbit,
    MinAttributeTidbit,
    min_and_max_distance_trivia_processor,
    min_and_max_elevation_trivia_processor,
)
from active_statistics.trivia.trivia import TriviaProcessor
from tests.factories.activity_factories import ActivityFactory


def test_min_and_max_distance_trivia(some_basic_runs_and_rides) -> None:
    """
    A basic test to make sure that if we pump some random data through the
    processor, nothing breaks.
    """
    min_and_max_distance_trivia_processor.get_data(some_basic_runs_and_rides)


def test_min_and_max_elevation_trivia(some_basic_runs_and_rides) -> None:
    """
    A basic test to make sure that if we pump some random data through the
    processor, nothing breaks.
    """
    min_and_max_elevation_trivia_processor.get_data(some_basic_runs_and_rides)


class TestMinAttributeTidbit:
    def test_activity_types_with_only_zero_for_distances_are_filtered_out(self) -> None:
        """
        Tests to make sure that if all activities return a distance of zero, that trivia data isn't returned.
        """
        processor = TriviaProcessor()
        processor.register_tidbit(
            MinAttributeTidbit(activity_type="Workout", attribute_name="distance")
        )

        workout_activity: Activity = ActivityFactory(type="Workout", distance=0.0)
        workout_activity_2: Activity = ActivityFactory(type="Workout", distance=0.0)
        activities = [workout_activity, workout_activity_2]

        data = processor.get_data(activity for activity in activities)

        assert data == []

    def test_activity_types_are_correctly_filtered_out(self) -> None:
        """
        Test to make sure that activities of other types are filtered out.
        """
        processor = TriviaProcessor()
        processor.register_tidbit(
            MinAttributeTidbit(activity_type="Run", attribute_name="distance")
        )

        run_activity: Activity = ActivityFactory(type="Run", distance=2.0)
        ride_activity: Activity = ActivityFactory(type="Ride", distance=1.0)
        activities = [run_activity, ride_activity]

        data = processor.get_data(activity for activity in activities)

        assert data[0][1] == "2 meters"


class TestMaxAttributeTidbit:
    def test_activity_types_with_only_zero_for_distances_are_filtered_out(self) -> None:
        """
        Tests to make sure that if all activities return a distance of zero, that trivia data isn't returned.
        """

        processor = TriviaProcessor()
        processor.register_tidbit(
            MaxAttributeTidbit(activity_type="Workout", attribute_name="distance")
        )

        workout_activity = ActivityFactory(type="Workout", distance=0.0)
        workout_activity_2 = ActivityFactory(type="Workout", distance=0.0)
        activities = [workout_activity, workout_activity_2]

        data = processor.get_data(activity for activity in activities)

        assert data == []

    def test_activity_types_are_correctly_filtered_out(self) -> None:
        """
        Test to make sure that activities of other types are filtered out.
        """
        processor = TriviaProcessor()
        processor.register_tidbit(
            MaxAttributeTidbit(activity_type="Run", attribute_name="distance")
        )

        run_activity = ActivityFactory(type="Run", distance=1.0)
        ride_activity = ActivityFactory(type="Ride", distance=2.0)
        activities = [run_activity, ride_activity]

        data = processor.get_data(activity for activity in activities)

        assert data[0][1] == "1 meters"
