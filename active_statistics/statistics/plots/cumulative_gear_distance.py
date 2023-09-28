import dataclasses
import datetime as dt
import itertools
from collections import defaultdict
from typing import Any, Iterator, Optional

import plotly.graph_objects as go
from stravalib import unithelper as uh
from stravalib.model import Activity, ActivityType

ALL_ACTIVITIES = "All"


@dataclasses.dataclass
class CompactActivity:
    type: ActivityType
    start_date_local: dt.datetime
    distance: uh.Quantity
    gear_id: str
    gear_name: str


def plot(activity_iterator: Iterator[Activity]) -> go.Figure:
    compact_activities: list[CompactActivity] = get_compact_activities(
        activity_iterator
    )

    # Sort activities into chronological order
    compact_activities.sort(key=lambda activity: activity.start_date_local)

    gear_id_to_name_mapping = {
        activity.gear_id: activity.gear_name for activity in compact_activities
    }

    # Get set of all the different types of activities this person has logged.
    activity_types = set(activity.type for activity in compact_activities)

    all_plots: dict[ActivityType, dict[str, go.Scatter]] = {}

    # Make plots for all activities
    all_plots[ALL_ACTIVITIES] = plot_graph(compact_activities)

    # Make plots for specific activities
    for activity_type in activity_types:
        all_plots[activity_type] = plot_graph(
            list(
                filter(
                    lambda activity: activity.type == activity_type, compact_activities
                )
            ),
        )

    data = get_figure_data_from_all_activity_data(all_plots, gear_id_to_name_mapping)
    layout = get_layout_from_all_activity_data(all_plots)

    fig = go.Figure(data=data, layout=layout)
    return fig


def get_compact_activities(
    activity_iterator: Iterator[Activity],
) -> list[CompactActivity]:
    return [
        CompactActivity(
            type=activity.type,
            start_date_local=activity.start_date_local,
            distance=activity.distance,
            gear_id=activity.gear_id,
            gear_name=activity.gear.name,
        )
        for activity in activity_iterator
        if activity.start_date_local is not None
        and activity.distance is not None
        and activity.gear_id is not None
        and activity.gear.name is not None
    ]


def plot_graph(
    activities: list[CompactActivity],
) -> dict[str, go.Scatter]:
    start_time_arrays: dict[str, list[dt.datetime]] = defaultdict(list)
    distance_arrays: dict[str, list[float]] = defaultdict(list)
    for activity in activities:
        start_time_arrays[activity.gear_id].append(activity.start_date_local)
        distance_arrays[activity.gear_id].append(activity.distance)

    for gear_id, times in distance_arrays.items():
        distance_arrays[gear_id] = list(itertools.accumulate(times))

    for gear_id, times in distance_arrays.items():
        # Convert distance from meters to km.
        distance_arrays[gear_id] = [x / 1000 for x in times]

    dd = {}

    # We want to iterate through the data by year, in reverse chronological order.
    # This ensures the scatter plots are generated in order.
    for gear_id, date in sorted(
        start_time_arrays.items(), key=lambda t: t[1][0], reverse=True
    ):
        dd[gear_id] = go.Scatter(
            x=date,
            y=distance_arrays[gear_id],
            hovertemplate="<b>Kilometers</b>: %{y:.0f}<br>",
            mode="lines",
        )

    return dd


def get_title_for_activity_type(activity_type: Optional[str]) -> str:
    if activity_type:
        return f"Cumulative Time Spent on {activity_type} Activities"
    else:
        return "Time Logged on Strava by Year"


def get_figure_data_from_all_activity_data(
    all_data: dict[ActivityType, dict[str, go.Scatter]],
    gear_id_to_gear_name_mapping: dict[str, str],
) -> list[go.Scatter]:
    figure_data: list[go.Scatter] = []

    for activity_type, scatters in all_data.items():
        for gear_id, scatter in scatters.items():
            if activity_type != ALL_ACTIVITIES:
                scatter.visible = False
            scatter.name = gear_id_to_gear_name_mapping[gear_id]
            figure_data.append(scatter)
    return figure_data


def get_layout_from_all_activity_data(
    all_data: dict[ActivityType, dict[str, go.Scatter]]
) -> dict[str, Any]:
    updatemenus = list(
        [
            dict(
                direction="left",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="center",
                y=1.02,
                yanchor="bottom",
                type="buttons",
                active=-1,
                buttons=list(
                    [
                        dict(
                            label=f"{activity_type}",
                            method="update",
                            args=[
                                {"visible": get_visible_array(all_data, activity_type)},
                                {
                                    "title": f"Cumulative Time Spent Using Certain Gear on {activity_type} Activities"
                                },
                            ],
                        )
                        for activity_type, _ in all_data.items()
                    ]
                ),
            )
        ]
    )

    layout = dict(
        title=f"Cumulative Distance for Different Gear",
        title_x=0.5,
        updatemenus=updatemenus,
        xaxis_title="Date",
        yaxis_title="Distance",
    )

    return layout


def get_visible_array(
    all_data: dict[ActivityType, dict[str, go.Scatter]],
    activity_type_button: ActivityType,
) -> list[bool]:
    visibility_list = []

    for activity_type, scatters in all_data.items():
        for year, scatter in scatters.items():
            visibility_list.append(activity_type == activity_type_button)

    return visibility_list


# For testing
if __name__ == "__main__":
    from active_statistics.utils import local_storage

    activity_iterator = local_storage.get_activity_iterator(94896104)
    f = plot(activity_iterator)
    f.show()
