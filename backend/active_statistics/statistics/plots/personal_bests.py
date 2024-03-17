"""
Plot your personal bests over time.
"""

import dataclasses
import datetime as dt
from collections import defaultdict
from typing import Iterator, Optional

import plotly.graph_objects as go
from active_statistics.exceptions import UserVisibleException
from stravalib.model import Activity, ActivityType


@dataclasses.dataclass
class CompactBestEffort:
    name: Optional[str]
    start_date_local: Optional[dt.timedelta]
    elapsed_time: Optional[int]


@dataclasses.dataclass
class CompactActivity:
    type: ActivityType
    best_efforts: Optional[list[CompactBestEffort]]


# Best efforts have names like: "400m" or "2 Mile". This just makes typing a little easier to understand.
BestEffortName = str


def plot(activity_iterator: Iterator[Activity]) -> go.Figure:
    activities = get_list_of_compact_activities(activity_iterator)

    activity_types = set(activity.type for activity in activities)

    data: dict[ActivityType, list[tuple[str, go.Scatter]]] = {}
    for activity_type in activity_types:
        data[activity_type] = plot_graph_per_activity(activities, activity_type)

    # Since runs are the only activity type for now with best efforts, lets just ignore everything else.
    if "Run" not in data:
        raise UserVisibleException("No runs found, so this plot can not be generated.")
    run_data: list[tuple[str, go.Scatter]] = data["Run"]

    layout = {
        "title": "Personal Bests over 400m",
        "title_x": 0.5,
        "xaxis_title": "Date",
        "yaxis_title": "Time (H:M:S)",
        "showlegend": False,
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
                "y": 1.02,
                "yanchor": "bottom",
                "buttons": list(
                    [
                        dict(
                            label=name,
                            method="update",
                            args=[
                                {
                                    "visible": get_list_of_falses_with_one_true(
                                        len(run_data), i
                                    )
                                },
                                {"title": f"Personal Bests over {name}"},
                            ],
                        )
                        for i, (name, _) in enumerate(run_data)
                    ]
                ),
            }
        ],
    }

    run_data = list(map(lambda x: x[1], run_data))
    make_only_first_scatter_visible(run_data)

    fig = go.Figure(data=run_data, layout=layout)
    fig.update_yaxes(tickformat="%H:%M:%S")
    return fig


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

        if activity.best_efforts is not None:
            compact_best_efforts = [
                CompactBestEffort(
                    name=best_effort.name,
                    start_date_local=best_effort.start_date_local,
                    elapsed_time=best_effort.elapsed_time,
                )
                for best_effort in activity.best_efforts
            ]
            compact_activities.append(
                CompactActivity(type=activity.type, best_efforts=compact_best_efforts)
            )
    return compact_activities


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


def make_only_first_scatter_visible(scatters: list[go.Scatter]) -> None:
    for i, scatter in enumerate(scatters):
        if i > 0:
            scatter.visible = False


def plot_graph_per_activity(
    activities: list[Activity], activity_type: ActivityType
) -> list[tuple[str, go.Scatter]]:
    # Only use activities of the selected activity type.
    activities = list(filter(lambda x: x.type == activity_type, activities))

    # Sort all best efforts into a dict[str, list[dt.datetime, dt.timedelta]]
    best_efforts_all_activities: dict[
        BestEffortName, list[tuple[dt.datetime, dt.timedelta]]
    ] = defaultdict(list)
    for activity in activities:
        if activity.best_efforts is not None:
            for best_effort in activity.best_efforts:
                best_efforts_all_activities[best_effort.name].append(
                    (best_effort.start_date_local, best_effort.elapsed_time)
                )

    # If there are no best efforts, just return because we have nothing to plot.
    if not best_efforts_all_activities:
        return []

    # Create data to plot
    data: list[tuple[str, go.Scatter]] = []
    for name, best_efforts in best_efforts_all_activities.items():
        data.append(plot_graph_per_length(name, best_efforts, activity_type))

    return data


def plot_graph_per_length(
    name: str,
    best_efforts: list[tuple[dt.datetime, dt.timedelta]],
    activity_type: ActivityType,
) -> tuple[str, go.Scatter]:
    fastest_time = dt.timedelta(seconds=1_000_000)

    # Create a list of all the personal best's we've gotten
    pbs: list[tuple[dt.datetime, dt.timedelta]] = []
    for date, elapsed_time in sorted(best_efforts, key=lambda x: x[0]):
        if elapsed_time < fastest_time:
            fastest_time = elapsed_time
            pbs.append((date, elapsed_time))

    # Add another point at today's date, so all plots continue to the present.
    if pbs[-1][0].date != dt.datetime.now().date:
        now = dt.datetime.now()
        today = dt.datetime(year=now.year, month=now.month, day=now.day)
        pbs.append((today, pbs[-1][1]))

    # Generate opacitites for each point, so that the last point is fully opaque.
    marker_opacity = [1] * len(pbs)
    marker_opacity[-1] = 0

    # Generate scatter plots and return
    return (
        name,
        go.Scatter(
            x=[pb[0] for pb in pbs],
            y=[dt.datetime(1970, 1, 1) + pb[1] for pb in pbs],
            line_shape="hv",
            marker={"opacity": marker_opacity},
            name=name,
            hovertemplate="Date: %{x}<br></b>Time: %{y|%H:%M:%S}",
        ),
    )


# For testing
if __name__ == "__main__":
    from active_statistics.utils import local_storage

    activity_iterator = local_storage.get_activity_iterator(94896104)
    f = plot(activity_iterator)

    # Uncomment the following to update the chart on the home page.

    # import json
    # import plotly

    # chart_json = json.dumps(f, cls=plotly.utils.PlotlyJSONEncoder)
    # with open(
    #     "./active_statistics/static/example_charts/personal_bests.json", "w"
    # ) as fp:
    #     fp.write(chart_json)

    f.show()
