from active_statistics.statistics.tables import top_hundred


class TestTopHundredLongestRuns:
    def test_cumulative_time_spent(self, some_basic_runs_and_rides) -> None:
        table_function = top_hundred.get_top_hundred_table_function(
            "Run",
            "distance",
            "Distance (km)",
            top_hundred.distance_conversion_function_to_km,
        )
        table_function(some_basic_runs_and_rides)

    def test_no_data(self, no_activities_at_all) -> None:
        table_function = top_hundred.get_top_hundred_table_function(
            "Run",
            "distance",
            "Distance (km)",
            top_hundred.distance_conversion_function_to_km,
        )
        table_function(no_activities_at_all)


class TestTopHundredLongestRides:
    def test_cumulative_time_spent(self, some_basic_runs_and_rides) -> None:
        table_function = top_hundred.get_top_hundred_table_function(
            "Ride",
            "distance",
            "Distance (km)",
            top_hundred.distance_conversion_function_to_km,
        )
        table_function(some_basic_runs_and_rides)

    def test_no_data(self, no_activities_at_all) -> None:
        table_function = top_hundred.get_top_hundred_table_function(
            "Ride",
            "distance",
            "Distance (km)",
            top_hundred.distance_conversion_function_to_km,
        )
        table_function(no_activities_at_all)
