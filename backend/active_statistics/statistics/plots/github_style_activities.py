import datetime as dt
from collections import Counter
from pathlib import Path
from typing import Iterator

import pandas as pd
import plotly.graph_objects as go
from active_statistics.exceptions import UserVisibleException
from plotly_calplot import calplot
from stravalib.model import Activity

CMAP = "YlGn"


def plot(activity_iterator: Iterator[Activity]) -> go.Figure:
    activity_dates = [activity.start_date_local for activity in activity_iterator]

    if not activity_dates:
        raise UserVisibleException(
            "Can't find any activities, so can't generate this plot."
        )

    earliest_activity = min(activity_dates)
    latest_activity = max(activity_dates)

    activity_counter = Counter(
        dt.datetime(activity_date.year, activity_date.month, activity_date.day)
        for activity_date in activity_dates
    )

    earliest_day = dt.datetime(earliest_activity.year, 1, 1)
    latest_day = dt.datetime(latest_activity.year, 12, 31)

    data = []
    day = earliest_day
    while day <= latest_day:
        data.append(
            {
                "date": day,
                "num_activities": activity_counter[day],
            }
        )
        day += dt.timedelta(days=1)

    df = pd.DataFrame(data)

    space_between_plots = get_space_between_plots(df)

    fig = calplot(
        df, x="date", y="num_activities", space_between_plots=space_between_plots
    )
    return fig


def get_space_between_plots(df: pd.DataFrame) -> float:
    """
    If we have a huge number of plots, we need to reduce the spacing between
    them so that the whole page isn't just spacing.
    """
    num_plots = max(df.date).year - min(df.date).year + 1
    return 0.02 if num_plots > 8 else 0.08


# For testing
if __name__ == "__main__":
    from active_statistics.utils import local_storage

    activity_iterator = local_storage.get_activity_iterator(94896104)
    f = plot(activity_iterator)
    f.show()
