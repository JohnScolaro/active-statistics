from active_statistics.statistics.plots.cumulative_distance_travelled import plot


def test_cumulative_time_spent(some_basic_runs_and_rides) -> None:
    plot(some_basic_runs_and_rides)


def test_no_data(no_activities_at_all) -> None:
    plot(no_activities_at_all)
