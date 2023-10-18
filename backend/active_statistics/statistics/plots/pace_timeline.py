"""
A line plot of the pace you've ran over consecutive runs, along with moving averages. An attempt to convince yourself
that you're getting faster.

TODO: Marker color proportional to length of activity.
"""
import dataclasses
import datetime as dt
import math
from typing import Iterator

import pandas as pd
import plotly.graph_objects as go
from active_statistics.exceptions import UserVisibleException
from active_statistics.statistics.utils.average_speed_utils import get_y_axis_settings
from stravalib import unithelper as uh
from stravalib.model import Activity, ActivityType


@dataclasses.dataclass
class CompactActivity:
    type: ActivityType
    average_speed: uh.Quantity
    start_date_local: dt.datetime
    moving_time: int


def plot(activity_iterator: Iterator[Activity]) -> go.Figure:
    activities: list[CompactActivity] = get_list_of_compact_activities(
        activity_iterator
    )

    if not activities:
        raise UserVisibleException("No data, so can't generate this plot.")

    alphabetical_activity_types = sorted(
        list(set(activity.type for activity in activities))
    )

    ordered_activities: dict[ActivityType, list[CompactActivity]] = {}
    for activity_type in alphabetical_activity_types:
        ordered_activities[activity_type] = sorted(
            (activity for activity in activities if activity.type == activity_type),
            key=lambda x: x.start_date_local,
        )

    data_scatters: list[tuple[ActivityType, go.Scatter]] = get_data_scatters(
        ordered_activities
    )
    moving_average_scatters: list[
        tuple[ActivityType, go.Scatter]
    ] = get_moving_average_scatters(ordered_activities, weighted=False)
    weighted_moving_average_scatters: list[
        tuple[ActivityType, go.Scatter]
    ] = get_moving_average_scatters(ordered_activities, weighted=True)

    layout = {
        "title": "Pace Timeline",
        "title_x": 0.5,
        "xaxis_title": "Date",
        "showlegend": True,
        "autosize": True,
        "updatemenus": [
            {
                "type": "buttons",
                "active": -1,
                "direction": "left",
                "pad": {"r": 10, "t": 10},
                "showactive": True,
                "x": 0.5,
                "xanchor": "center",
                "y": 1.04,
                "yanchor": "middle",
                "buttons": [
                    dict(
                        label=activity_type,
                        method="update",
                        args=[
                            {
                                "visible": get_list_of_falses_with_one_true(
                                    len(data_scatters), i
                                )
                                * 3
                            },
                            {
                                "yaxis": {
                                    "tickformat": get_y_axis_settings(
                                        activity_type
                                    ).tick_format,
                                    "title": get_y_axis_settings(
                                        activity_type
                                    ).axis_title,
                                }
                            },
                        ],
                    )
                    for i, (activity_type, scatter) in enumerate(data_scatters)
                ],
            },
        ],
    }

    fig = go.Figure(
        data=[scatter for _, scatter in data_scatters]
        + [scatter for _, scatter in moving_average_scatters]
        + [scatter for _, scatter in weighted_moving_average_scatters],
        layout=layout,
    )

    set_initial_y_axis(fig)

    return fig


def get_data_scatters(
    ordered_activities: dict[ActivityType, list[CompactActivity]]
) -> list[go.Figure]:
    data_scatters: list[tuple[ActivityType, list[CompactActivity]]] = []

    for i, (activity_type, activities) in enumerate(ordered_activities.items()):
        pace_conversion_function = get_y_axis_settings(
            activity_type
        ).conversion_function
        x = [activity.start_date_local for activity in activities]
        y = [
            pace_conversion_function(activity.average_speed) for activity in activities
        ]
        data_scatters.append(
            (
                activity_type,
                go.Scatter(
                    name=activity_type,
                    x=x,
                    y=y,
                    visible=(i == 0),
                    mode="markers",
                ),
            )
        )

    return data_scatters


def get_moving_average_scatters(
    ordered_activities: dict[ActivityType, list[CompactActivity]], weighted: bool
) -> list[go.Figure]:
    scatters: list[go.Scatter] = []
    for i, (activity_type, activities) in enumerate(ordered_activities.items()):
        pace_conversion_function = get_y_axis_settings(
            activity_type
        ).conversion_function
        x = [activity.start_date_local for activity in activities]
        y = [activity.average_speed.m for activity in activities]
        moving_time = [
            activity.moving_time if weighted else 1.0 for activity in activities
        ]
        moving_average_x, moving_average_y = generate_weighted_moving_average(
            x, y, moving_time
        )
        converted_moving_average_y = [
            pace_conversion_function(uh.Quantity(i, "m/s")) for i in moving_average_y
        ]

        scatters.append(
            (
                activity_type,
                go.Scatter(
                    name=f"30 Day {'Weighted ' if weighted else ''}Moving Average",
                    x=moving_average_x,
                    y=converted_moving_average_y,
                    mode="lines",
                    visible=(i == 0),
                ),
            )
        )

    return scatters


def generate_weighted_moving_average(
    datetimes: list[dt.datetime], values: list[float], weights: list[float]
) -> tuple[list[dt.datetime], list[float]]:
    df = pd.DataFrame({"datetime": datetimes, "values": values, "weights": weights})
    df = df.set_index("datetime")

    # Re-sample into days using the weights to average days with multiple activities.
    resampled_weights = df["weights"].resample("D").sum()
    resampled_values = (df["values"] * df["weights"]).resample(
        "D"
    ).sum() / resampled_weights
    daily_data = pd.DataFrame(
        {"values": resampled_values, "weights": resampled_weights}
    )

    # Iterate over the dates, calculating the weighted values for each window.
    dates = []
    values = []
    for date in daily_data.index:
        group = daily_data[date - dt.timedelta(days=15) : date + dt.timedelta(days=15)]
        dates.append(date)
        values.append(
            (group["values"] * group["weights"]).sum() / group["weights"].sum()
        )

    # Keep only 1 contiguous "None" row. A single "None" row is enough to stop plotly from joining the moving averages
    # together over long gaps, we don't want to create extra data for nothing, so drop the multiples.
    final_dates: list[dt.datetime] = []
    final_values: list[float] = []
    for date, value in zip(dates, values):
        if (
            len(final_values) != 0
            and math.isnan(value)
            and math.isnan(final_values[-1])
        ):
            continue
        else:
            final_dates.append(date)
            final_values.append(value)

    return (final_dates, final_values)


def get_list_of_falses_with_one_true(len_list: int, index_of_true: int) -> list[bool]:
    """
    Helper to get a list like: [False, True, False, False] for parameters of (4, 1).
    Used to get visibility of buttons.
    """
    a = []
    for i in range(len_list):
        if i == index_of_true:
            a.append(True)
        else:
            a.append(False)
    return a


def get_list_of_compact_activities(
    activity_iterator: Iterator[Activity],
) -> list[CompactActivity]:
    """
    To save data, we don't want to load everything from every detailed activity. Just the information we need.
    """
    compact_activities: list[CompactActivity] = []
    for activity in activity_iterator:
        # We don't want to include flagged activities
        if activity.flagged:
            continue

        # We also can't generate this plot for activities were the start date or the average speed are None.
        if activity.start_date_local is None or activity.average_speed is None:
            continue

        # We also can't generated weighted average lines if we're missing the moving time.
        if activity.moving_time is None:
            continue

        compact_activities.append(
            CompactActivity(
                type=activity.type,
                average_speed=activity.average_speed,
                start_date_local=activity.start_date_local,
                moving_time=activity.moving_time.total_seconds(),
            )
        )

    return compact_activities


def set_initial_y_axis(fig: go.Figure) -> None:
    """
    If the y axis format is set to something incorrect (for example "%M:%S" when the data is actually numeric) then
    plotly defaults to displaying the y axis as a percentage. This sets the initial yaxis format to be correct.
    """
    first_activity_type = fig["data"][0]["name"]

    fig["layout"]["yaxis"]["tickformat"] = get_y_axis_settings(
        first_activity_type
    ).tick_format


# For testing
if __name__ == "__main__":
    from active_statistics.utils import local_storage

    activity_iterator = local_storage.get_activity_iterator(94896104)
    fig = plot(activity_iterator)

    fig.show()
