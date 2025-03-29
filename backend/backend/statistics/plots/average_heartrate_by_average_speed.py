import dataclasses
import datetime as dt
from typing import Any, Callable, Iterator, Optional

import plotly.graph_objects as go
from stravalib import unit_helper as uh
from stravalib.model import ActivityType, DetailedActivity

from backend.exceptions import UserVisibleError
from backend.statistics.utils.average_speed_utils import (
    average_speed_to_kmph,
    average_speed_to_mins_per_km,
)


@dataclasses.dataclass
class CompactActivity:
    type: ActivityType
    start_date: dt.datetime
    average_heartrate: float
    average_speed: float
    distance: uh._Quantity


def plot(activity_iterator: Iterator[DetailedActivity]) -> go.Figure:
    compact_activities: list[CompactActivity] = get_compact_activities(
        activity_iterator
    )
    # Sort activities by start date.
    compact_activities.sort(key=lambda activity: activity.start_date)

    runs: list[CompactActivity] = [
        activity
        for activity in compact_activities
        if activity.type == "Run" and activity.average_heartrate is not None
    ]

    rides: list[CompactActivity] = [
        activity
        for activity in compact_activities
        if activity.type == "Ride" and activity.average_heartrate is not None
    ]

    if not runs and not rides:
        raise UserVisibleError(
            (
                "There are no runs and no rides with heartrate, so this plot can not "
                "be generated."
            )
        )

    scatters = []
    if runs:
        run_scatter = get_scatter_plot("Run", runs)
        scatters.append(run_scatter)

    if rides:
        ride_scatter = get_scatter_plot("Ride", rides)
        scatters.append(ride_scatter)

    example_layout = {
        "title": "Average Heartrate vs Average Pace",
        "xaxis_title": "Average Heartrate (bpm)",
        "yaxis_title": "Average Pace (mins/km)",
        "yaxis": {"tickformat": "%M:%S"},
        "title_x": 0.5,
        "showlegend": False,
        "updatemenus": [
            {
                "type": "buttons",
                "active": -1,
                "direction": "left",
                "pad": {"r": 10, "t": 10},
                "showactive": True,
                "x": 0.5,
                "xanchor": "center",
                "y": 1.02,
                "yanchor": "bottom",
                "buttons": get_buttons(bool(runs), bool(rides)),
            }
        ],
    }

    # Set default
    for scatter in scatters:
        scatter.update({"visible": False})
    scatters[0].update({"visible": True})

    fig = go.Figure(data=scatters, layout=example_layout)

    fig.update_coloraxes()
    return fig


def get_compact_activities(
    activity_iterator: Iterator[DetailedActivity],
) -> list[CompactActivity]:
    compact_activities: list[CompactActivity] = []

    for activity in activity_iterator:
        # If the activity is missing any of:
        #   * start date
        #   * average heartrate
        #   * average speed, we can't color, or plot it, so discard these activities.
        if (
            activity.start_date is None
            or activity.average_heartrate is None
            or activity.average_speed is None
        ):
            continue

        compact_activities.append(
            CompactActivity(
                type=activity.type.root,
                start_date=activity.start_date,
                average_heartrate=activity.average_heartrate,
                average_speed=activity.average_speed,
                distance=activity.distance,
            )
        )
    return compact_activities


def get_scatter_plot(
    activity_type: ActivityType,
    activities: list[CompactActivity],
) -> go.Figure:
    speed_conversion_function = get_speed_conversion_function(activity_type)

    average_heartrates: list[float] = []
    average_paces: list[float] = []
    for activity in activities:
        speed = speed_conversion_function(activity.average_speed)
        if speed is not None:
            average_heartrates.append(activity.average_heartrate)
            average_paces.append(speed)

    start_times = [activity.start_date for activity in activities]
    start_timestamps = [int(start_time.timestamp()) for start_time in start_times]
    distances_in_km = [activity.distance / 1000 for activity in activities]

    # Scale by an arbitrary number to make this look better.
    scaled_distances_for_size = [d * 20 for d in distances_in_km]

    tickvals = list(
        range(
            min(start_timestamps),
            max(start_timestamps),
            # The outter max is stopping this from going below 1, which can
            # happen in cases of very few activities.
            max(1, (max(start_timestamps) - min(start_timestamps)) // 5),
        )
    )
    ticktext = [dt.datetime.fromtimestamp(i).strftime("%d/%m/%Y") for i in tickvals]

    return go.Scatter(
        x=average_heartrates,
        y=average_paces,
        customdata=list(zip(distances_in_km, start_times)),
        mode="markers",
        marker={
            "size": scaled_distances_for_size,
            "color": start_timestamps,
            "showscale": True,  # Shows the colorbar
            "sizemode": "area",
            "colorbar": {
                "title": "Date of Activity",
                "tickmode": "array",
                "ticktext": ticktext,
                "tickvals": tickvals,
            },
        },
        hovertemplate="Average Heartrate: %{x} bpm<br>"
        + get_hovertemplate_pace_formatting(activity_type)
        + "Distance: %{customdata[0]:.2f}km<br>"
        + "Date: %{customdata[1]|%d-%m-%Y}<br>"
        + "<extra></extra>",
    )


def get_speed_conversion_function(
    activity_type: ActivityType,
) -> Callable[[float], Optional[Any]]:
    if activity_type == "Run":
        return average_speed_to_mins_per_km
    else:
        return average_speed_to_kmph


def get_hovertemplate_pace_formatting(activity_type: ActivityType) -> str:
    if activity_type == "Run":
        return "Average Pace: %{y|%-M:%S}/km<br>"
    else:
        return "Average Pace: %{y}kmph<br>"


def get_buttons(runs: bool, rides: bool) -> list[Any]:
    num_activities_to_make_buttons_for = [runs, rides].count(True)
    buttons: list[dict[str, Any]] = []
    if runs:
        buttons.append(
            {
                "label": "Run",
                "method": "update",
                "args": [
                    {"visible": [False] * num_activities_to_make_buttons_for},
                    {
                        "yaxis": {
                            "tickformat": "%M:%S",
                            "title": "Average Pace (mins/km)",
                        }
                    },
                ],
            },
        )

    if rides:
        buttons.append(
            {
                "label": "Ride",
                "method": "update",
                "args": [
                    {"visible": [False] * num_activities_to_make_buttons_for},
                    {
                        "yaxis": {
                            "tickformat": None,
                            "title": "Average Pace (kmph)",
                        }
                    },
                ],
            },
        )

    for i, button in enumerate(buttons):
        button["args"][0]["visible"][i] = True

    return buttons


# For testing
if __name__ == "__main__":
    from backend.utils import local_storage

    activity_iterator = local_storage.get_activity_iterator(94896104)
    f = plot(activity_iterator)
    f.show()
