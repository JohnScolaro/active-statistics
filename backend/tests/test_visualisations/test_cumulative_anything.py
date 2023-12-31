from active_statistics.statistics.plots import cumulative_anything


class TestCumulativeTimeSpent:
    def test_cumulative_time_spent(self, some_basic_runs_and_rides) -> None:
        plot_function = cumulative_anything.get_plot_function(
            "moving_time",
            cumulative_anything.conversion_function_for_timedeltas,
            "Hours",
            cumulative_anything.get_title_for_cumulative_time_plot,
        )
        plot_function(some_basic_runs_and_rides)

    def test_no_data(self, no_activities_at_all) -> None:
        plot_function = cumulative_anything.get_plot_function(
            "moving_time",
            cumulative_anything.conversion_function_for_timedeltas,
            "Hours",
            cumulative_anything.get_title_for_cumulative_time_plot,
        )
        plot_function(no_activities_at_all)


class TestCumulativeDistance:
    def test_cumulative_time_spent(self, some_basic_runs_and_rides) -> None:
        plot_function = cumulative_anything.get_plot_function(
            "distance",
            cumulative_anything.conversion_function_for_distance_to_km,
            "Kilometers",
            cumulative_anything.get_title_for_cumulative_distance_plot,
        )
        plot_function(some_basic_runs_and_rides)

    def test_no_data(self, no_activities_at_all) -> None:
        plot_function = cumulative_anything.get_plot_function(
            "distance",
            cumulative_anything.conversion_function_for_distance_to_km,
            "Kilometers",
            cumulative_anything.get_title_for_cumulative_distance_plot,
        )
        plot_function(no_activities_at_all)


class TestCumulativeElevation:
    def test_cumulative_time_spent(self, some_basic_runs_and_rides) -> None:
        plot_function = cumulative_anything.get_plot_function(
            "total_elevation_gain",
            cumulative_anything.conversion_function_for_distance_to_m,
            "Meters",
            cumulative_anything.get_title_for_cumulative_elevation_plot,
        )
        plot_function(some_basic_runs_and_rides)

    def test_no_data(self, no_activities_at_all) -> None:
        plot_function = cumulative_anything.get_plot_function(
            "total_elevation_gain",
            cumulative_anything.conversion_function_for_distance_to_m,
            "Meters",
            cumulative_anything.get_title_for_cumulative_elevation_plot,
        )
        plot_function(no_activities_at_all)


class TestCumulativeKudos:
    def test_cumulative_time_spent(self, some_basic_runs_and_rides) -> None:
        plot_function = cumulative_anything.get_plot_function(
            "kudos_count",
            cumulative_anything.conversion_function_for_int,
            "Kudos",
            cumulative_anything.get_title_for_cumulative_kudos_plot,
        )
        plot_function(some_basic_runs_and_rides)

    def test_no_data(self, no_activities_at_all) -> None:
        plot_function = cumulative_anything.get_plot_function(
            "kudos_count",
            cumulative_anything.conversion_function_for_int,
            "Kudos",
            cumulative_anything.get_title_for_cumulative_kudos_plot,
        )
        plot_function(no_activities_at_all)
