from active_statistics.statistics.plots.cumulative_gear_distance import plot


def test_cumulative_gear_distance(some_basic_runs_and_rides) -> None:
    plot(some_basic_runs_and_rides)


def test_no_data(no_activities_at_all) -> None:
    plot(no_activities_at_all)
