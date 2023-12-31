from active_statistics.gui.tabs import (
    average_hr_by_average_speed_tab,
    calendar_tab,
    cumulative_distance_tab,
    cumulative_elevation_tab,
    cumulative_gear_distance_tab,
    cumulative_gear_time_tab,
    cumulative_kudos_tab,
    cumulative_time_tab,
    detailed_trivia_tab,
    flagged_activities_tab,
    general_trivia_tab,
    histogram_of_activity_times_tab,
    min_and_max_distance_activities_tab,
    min_and_max_elevation_activities_tab,
    pace_timeline_tab,
    personal_bests_tab,
    polyline_grid_tab,
    polyline_overlay_tab,
    top_100_longest_rides_tab,
    top_100_longest_runs_tab,
)
from active_statistics.tabs.tab_group import TabGroup
from active_statistics.tabs.tabs import Tab

tab_tree: list[Tab | TabGroup] = [
    TabGroup(
        name="Summary Data",
        key="summary_data",
        children=[
            TabGroup(
                name="Plots",
                key="summary_plots",
                children=[
                    cumulative_time_tab,
                    cumulative_distance_tab,
                    cumulative_elevation_tab,
                    cumulative_kudos_tab,
                    calendar_tab,
                    average_hr_by_average_speed_tab,
                    pace_timeline_tab,
                    histogram_of_activity_times_tab,
                ],
            ),
            TabGroup(
                name="Tables",
                key="summary_tables",
                children=[
                    min_and_max_distance_activities_tab,
                    min_and_max_elevation_activities_tab,
                    general_trivia_tab,
                    flagged_activities_tab,
                    top_100_longest_runs_tab,
                    top_100_longest_rides_tab,
                ],
            ),
            TabGroup(
                name="Images",
                key="summary_images",
                children=[
                    polyline_overlay_tab,
                    polyline_grid_tab,
                ],
            ),
        ],
    ),
    TabGroup(
        name="Detailed Data",
        key="detailed_data",
        children=[
            personal_bests_tab,
            cumulative_gear_time_tab,
            cumulative_gear_distance_tab,
            detailed_trivia_tab,
        ],
    ),
]


def get_all_tabs() -> list[Tab]:
    """
    Return a flattened list of all the tabs in the tab tree. Just the actual tabs, not the TabGroups.
    """

    def flatten(tabs: list[Tab | TabGroup]) -> list[Tab]:
        flattened_tabs = []
        for tab in tabs:
            if isinstance(tab, TabGroup):
                flattened_tabs.extend(flatten(tab.children))
            else:
                flattened_tabs.append(tab)
        return flattened_tabs

    return flatten(tab_tree)
