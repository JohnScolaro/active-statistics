import dataclasses
import datetime as dt
from typing import Iterator

import plotly.graph_objects as go
from stravalib.model import ActivityType, DetailedActivity

from backend.exceptions import UserVisibleException


@dataclasses.dataclass
class CompactActivity:
    type: ActivityType
    start_date_local: dt.datetime


def plot(activity_iterator: Iterator[DetailedActivity]) -> go.Figure:
    compact_activities: list[CompactActivity] = get_compact_activities(
        activity_iterator
    )

    if not compact_activities:
        raise UserVisibleException("No Data")

    activity_types = sorted(
        set(activity.type for activity in compact_activities), reverse=True
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
    activity_iterator: Iterator[DetailedActivity],
) -> list[CompactActivity]:
    return [
        CompactActivity(
            type=activity.type.root,
            start_date_local=activity.start_date_local,
        )
        for activity in activity_iterator
        if activity.start_date_local is not None
    ]


# For testing
if __name__ == "__main__":
    raise NotImplementedError("Testing locally not implemented yet")
