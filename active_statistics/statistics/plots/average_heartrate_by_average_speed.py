import dataclasses
import datetime as dt
from typing import Any, Callable, Iterator

import plotly.graph_objects as go
from stravalib import unithelper as uh
from stravalib.model import Activity, ActivityType

from active_statistics.exceptions import UserVisibleException


@dataclasses.dataclass
class CompactActivity:
    type: ActivityType
    start_date: dt.datetime
    average_heartrate: float
    average_speed: float
    distance: uh.meters


def plot(activity_iterator: Iterator[Activity]) -> go.Figure:
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
        raise UserVisibleException(
            "There are no runs and no rides with heartrate, so this plot can not be generated."
        )

    scatters = []
    if runs:
        run_scatter = get_scatter_plot("Run", runs)
        scatters.append(run_scatter)

    if rides:
        ride_scatter = get_scatter_plot("Ride", rides)
        scatters.append(ride_scatter)

    example_layout = {
        "title": f"Average Heartrate vs Average Pace",
        "xaxis_title": "Average Heartrate (bpm)",
        "yaxis_title": "Average Pace (mins/km)",
        "yaxis": {"tickformat": "%M:%S"},
        "title_x": 0.5,
        "showlegend": False,
        "updatemenus": [
            {
                "type": "buttons",
                "active": -1,
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
        scatter.update(dict(visible=False))
    scatters[0].update(dict(visible=True))

    fig = go.Figure(data=scatters, layout=example_layout)

    fig.update_coloraxes()
    return fig


def get_compact_activities(
    activity_iterator: Iterator[Activity],
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
                type=activity.type,
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

    average_heartrates = [activity.average_heartrate for activity in activities]
    average_paces: list[float] = [
        speed_conversion_function(activity.average_speed) for activity in activities
    ]

    # If this is a run activity, convert paces into times for nice formatting.
    if activity_type == "Run":
        average_paces_running: list[dt.datetime] = [
            dt.datetime(1970, 1, 1) + dt.timedelta(seconds=pace)
            for pace in average_paces
        ]

    start_times = [activity.start_date for activity in activities]
    start_timestamps = [int(start_time.timestamp()) for start_time in start_times]
    distances_in_km = [activity.distance.m / 1000 for activity in activities]

    # Scale by an arbitrary number to make this look better.
    scaled_distances_for_size = [d * 20 for d in distances_in_km]

    tickvals = [
        i
        for i in range(
            min(start_timestamps),
            max(start_timestamps),
            # The outter max is stopping this from going below 1, which can happen in cases of very few activities.
            max(1, (max(start_timestamps) - min(start_timestamps)) // 5),
        )
    ]
    ticktext = [dt.datetime.fromtimestamp(i).strftime("%d/%m/%Y") for i in tickvals]

    return go.Scatter(
        x=average_heartrates,
        y=average_paces if activity_type == "Ride" else average_paces_running,
        customdata=list(zip(distances_in_km, start_times)),
        mode="markers",
        marker=dict(
            size=scaled_distances_for_size,
            color=start_timestamps,
            showscale=True,  # Shows the colorbar
            sizemode="area",
            colorbar=dict(
                title="Date of Activity",
                tickmode="array",
                ticktext=ticktext,
                tickvals=tickvals,
            ),
        ),
        hovertemplate="Average Heartrate: %{x} bpm<br>"
        + get_hovertemplate_pace_formatting(activity_type)
        + "Distance: %{customdata[0]:.2f}km<br>"
        + "Date: %{customdata[1]|%d-%m-%Y}<br>"
        + "<extra></extra>",
    )


def meters_per_second_to_seconds_per_kilometer(speed: uh.Quantity) -> float:
    return float(1000 / speed.magnitude)


def meters_per_second_to_kilometers_per_hour(speed: uh.Quantity) -> float:
    return float(speed.magnitude / 1000 * 3600)


def get_speed_conversion_function(
    activity_type: ActivityType,
) -> Callable[[float], float]:
    if activity_type == "Run":
        return meters_per_second_to_seconds_per_kilometer
    else:
        return meters_per_second_to_kilometers_per_hour


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
            dict(
                label="Run",
                method="update",
                args=[
                    {"visible": [False] * num_activities_to_make_buttons_for},
                    {
                        "yaxis": {
                            "tickformat": "%M:%S",
                            "title": "Average Pace (mins/km)",
                        }
                    },
                ],
            ),
        )

    if rides:
        buttons.append(
            dict(
                label="Ride",
                method="update",
                args=[
                    {"visible": [False] * num_activities_to_make_buttons_for},
                    {
                        "yaxis": {
                            "tickformat": None,
                            "title": "Average Pace (kmph)",
                        }
                    },
                ],
            ),
        )

    for i, button in enumerate(buttons):
        button["args"][0]["visible"][i] = True

    return buttons


# For testing
if __name__ == "__main__":
    from active_statistics.utils import local_storage

    activity_iterator = local_storage.get_activity_iterator(94896104)
    f = plot(activity_iterator)
    f.show()
