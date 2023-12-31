import dataclasses
import datetime as dt
import itertools
from typing import Any, Callable, Iterator, Optional

import plotly.graph_objects as go
from stravalib import unithelper as uh
from stravalib.model import Activity, ActivityType

ALL_ACTIVITIES = "All"


@dataclasses.dataclass
class CompactActivity:
    type: ActivityType
    start_date_local: dt.datetime
    activity_attribute: Any


def get_plot_function(
    activity_attribute_name: str,
    conversion_function: Callable[[Any], Any],
    yaxis_title: str,
    plot_title_creator: Callable[[str], str],
) -> Callable[[Iterator[Activity]], go.Figure]:
    """
    Takes a few values to customize a tab, and returns a function that when
    called with an iterator of activities, returns a plotly figure of a
    cumulative plot about the attribute of interest.
    """

    def plot(activity_iterator: Iterator[Activity]) -> go.Figure:
        compact_activities: list[CompactActivity] = get_compact_activities(
            activity_attribute_name, activity_iterator, conversion_function
        )

        # Get set of all the different types of activities this person has logged.
        activity_types = set(activity.type for activity in compact_activities)

        all_plots: dict[ActivityType, dict[int, go.Scatter]] = {}

        # Make plots for all activities
        all_plots[ALL_ACTIVITIES] = plot_graph(compact_activities, yaxis_title)

        # Make plots for specific activities
        for activity_type in activity_types:
            all_plots[activity_type] = plot_graph(
                list(
                    filter(
                        lambda activity: activity.type == activity_type,
                        compact_activities,
                    )
                ),
                yaxis_title,
            )

        data = get_figure_data_from_all_activity_data(all_plots)
        layout = get_layout_from_all_activity_data(
            all_plots,
            yaxis_title=yaxis_title,
            plot_title_creator=plot_title_creator,
        )

        fig = go.Figure(data=data, layout=layout)
        return fig

    return plot


def get_compact_activities(
    activity_attribute_name: str,
    activity_iterator: Iterator[Activity],
    conversion_function: Callable[[Any], Any],
) -> list[CompactActivity]:
    return [
        CompactActivity(
            type=activity.type,
            start_date_local=activity.start_date_local,
            activity_attribute=conversion_function(
                getattr(activity, activity_attribute_name)
            ),
        )
        for activity in activity_iterator
        if activity.start_date_local is not None
        and getattr(activity, activity_attribute_name) is not None
    ]


def plot_graph(
    activities: list[CompactActivity], yaxis_title: str
) -> dict[int, go.Scatter]:
    graph_data: dict[int, list[float]] = {}
    for activity in activities:
        activity_datetime = activity.start_date_local
        year = activity_datetime.year
        year_data = graph_data.get(year, [0.0] * 366)
        year_data[
            activity_datetime.timetuple().tm_yday - 1
        ] += activity.activity_attribute
        graph_data[year] = year_data

    for year, year_data in graph_data.items():
        graph_data[year] = list(itertools.accumulate(year_data))

    # Remove additional zeros from end of data if year is the current year
    current_year = dt.datetime.now().year
    current_day = dt.datetime.now().timetuple().tm_yday - 1
    if current_year in graph_data:
        graph_data[current_year] = graph_data[current_year][0:current_day]

    dd = {}

    # We want to iterate through the data by year, in reverse chronological order.
    # This ensures the scatter plots are generated in order.
    for year, year_data in sorted(graph_data.items(), key=lambda t: t[0], reverse=True):
        dd[year] = go.Scatter(
            x=list(range(1, len(year_data) + 1)),
            y=year_data,
            customdata=tuple(
                dt.datetime(year, 1, 1) + dt.timedelta(days=i)
                for i in range(len(year_data))
            ),
            hovertemplate="<b>Date: %{customdata|%d %b %Y}</b><br>"
            + f"<b>{yaxis_title}</b>: %{{y:.0f}}<br>",
        )

    return dd


def get_title_for_activity_type(activity_type: Optional[str]) -> str:
    if activity_type:
        return f"Cumulative Time Spent on {activity_type} Activities"
    else:
        return "Time Logged on Strava by Year"


def get_figure_data_from_all_activity_data(
    all_data: dict[ActivityType, dict[int, go.Scatter]]
) -> list[go.Scatter]:
    figure_data: list[go.Scatter] = []

    for activity_type, scatters in all_data.items():
        for year, scatter in scatters.items():
            if activity_type != ALL_ACTIVITIES:
                scatter.visible = False
            scatter.name = str(year)
            figure_data.append(scatter)
    return figure_data


def get_layout_from_all_activity_data(
    all_data: dict[ActivityType, dict[int, go.Scatter]],
    yaxis_title: str,
    plot_title_creator: Callable[[str], str],
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
                                {"title": plot_title_creator(activity_type)},
                            ],
                        )
                        for activity_type, _ in all_data.items()
                    ]
                ),
            )
        ]
    )

    layout = dict(
        title=plot_title_creator(ALL_ACTIVITIES),
        title_x=0.5,
        updatemenus=updatemenus,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        xaxis=dict(
            tickmode="array",
            tickvals=[1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335],
            ticktext=[
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
        ),
    )

    return layout


def get_visible_array(
    all_data: dict[ActivityType, dict[int, go.Scatter]],
    activity_type_button: ActivityType,
) -> list[bool]:
    visibility_list = []

    for activity_type, scatters in all_data.items():
        for year, scatter in scatters.items():
            visibility_list.append(activity_type == activity_type_button)

    return visibility_list


def conversion_function_for_timedeltas(attribute_value: dt.timedelta) -> float:
    """
    Takes the moving_time timedelta and converts it to a float that represents
    hours.
    """
    return attribute_value.total_seconds() / 3600


def conversion_function_for_distance_to_km(attribute_value: uh.Quantity) -> uh.Quantity:
    """
    Converts a uh.Quantity representing meters into a float representing
    kilometers.
    """
    return uh.kilometers(attribute_value)


def conversion_function_for_distance_to_m(attribute_value: uh.Quantity) -> uh.Quantity:
    """
    Converts a uh.Quantity representing meters into a float representing
    meters.
    """
    return uh.meters(attribute_value)


def conversion_function_for_int(attribute_value: int) -> float:
    """
    The most boring conversion function. It does nothing.
    """
    return float(attribute_value)


def get_title_for_cumulative_time_plot(activity_type: str) -> str:
    return f"Cumulative Time Spent on {activity_type} Activities"


def get_title_for_cumulative_distance_plot(activity_type: str) -> str:
    return f"Cumulative Distance Travelled During {activity_type} Activities"


def get_title_for_cumulative_elevation_plot(activity_type: str) -> str:
    return f"Cumulative Elevation Climbed During {activity_type} Activities"


def get_title_for_cumulative_kudos_plot(activity_type: str) -> str:
    return f"Cumulative Kudos Achieved During {activity_type} Activities"


# For testing
if __name__ == "__main__":
    from active_statistics.utils import local_storage

    activity_iterator = local_storage.get_activity_iterator(94896104)
    plot_function = get_plot_function(
        "moving_time",
        conversion_function_for_timedeltas,
        "Hours",
        get_title_for_cumulative_time_plot,
    )
    fig = plot_function(activity_iterator)
    fig.show()
