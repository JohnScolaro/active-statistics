import dataclasses
import datetime as dt
from typing import Iterator

import plotly.graph_objects as go
from active_statistics.exceptions import UserVisibleException
from stravalib.model import Activity, ActivityType


@dataclasses.dataclass
class CompactActivity:
    type: ActivityType
    start_date_local: dt.datetime


def plot(activity_iterator: Iterator[Activity]) -> go.Figure:
    compact_activities: list[CompactActivity] = get_compact_activities(
        activity_iterator
    )

    if not compact_activities:
        raise UserVisibleException("No Data")

    activity_types = list(
        sorted(set(activity.type for activity in compact_activities), reverse=True)
    )

    histograms: list[go.Histogram] = []
    for activity_type in activity_types:
        histograms.append(
            go.Histogram(
                x=[
                    dt.datetime.combine(
                        date=dt.date(2000, 1, 1), time=activity.start_date_local.time()
                    )
                    for activity in compact_activities
                    if activity.type == activity_type
                ],
                nbinsx=24 * 4,
                name=activity_type,
                hovertemplate="<b>Time:</b> %{x}<br><b>Number of Activities:</b> %{y}",
            )
        )

    return go.Figure(
        data=histograms,
        layout=dict(
            xaxis_title="Time of Day",
            yaxis_title="Frequency",
            title="Histogram of Activity Start Times",
            barmode="stack",
            xaxis={"tickformat": "%H:%M"},
            title_x=0.5,
        ),
    )


def get_compact_activities(
    activity_iterator: Iterator[Activity],
) -> list[CompactActivity]:
    return [
        CompactActivity(
            type=activity.type,
            start_date_local=activity.start_date_local,
        )
        for activity in activity_iterator
        if activity.start_date_local is not None
    ]


# For testing
if __name__ == "__main__":
    from active_statistics.utils import local_storage

    activity_iterator = local_storage.get_activity_iterator(94896104)
    f = plot(activity_iterator)
    f.show()
