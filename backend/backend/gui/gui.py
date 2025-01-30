from backend.gui.tabs import (
    animated_polyline_grid_tab,
    average_hr_by_average_speed_tab,
    calendar_tab,
    cumulative_distance_tab,
    cumulative_elevation_tab,
    cumulative_kudos_tab,
    cumulative_time_tab,
    flagged_activities_tab,
    general_trivia_tab,
    histogram_of_activity_times_tab,
    min_and_max_distance_activities_tab,
    min_and_max_elevation_activities_tab,
    pace_timeline_tab,
    polyline_grid_tab,
    top_100_longest_rides_tab,
    top_100_longest_runs_tab,
)
from backend.tabs.tab_group import TabGroup
from backend.tabs.tabs import Tab

tab_tree: list[Tab | TabGroup] = [
    TabGroup(
        name="Visualisations",
        key="visualisations",
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
                children=[polyline_grid_tab, animated_polyline_grid_tab],
            ),
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
