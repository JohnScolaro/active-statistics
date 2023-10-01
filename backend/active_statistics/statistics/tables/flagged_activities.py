from typing import Iterator

import pandas as pd
from active_statistics.statistics.utils.strava_links import (
    get_activity_url,
    get_html_link,
)
from stravalib.model import Activity


def flagged_activities_table(activities: Iterator[Activity]) -> pd.DataFrame:
    flagged_activities = [activity for activity in activities if activity.flagged]

    activity_names = [activity.name for activity in flagged_activities]
    activity_links = [
        get_html_link(get_activity_url(activity.id)) for activity in flagged_activities
    ]

    return pd.DataFrame(
        {"Activity Names": activity_names, "Activity Links": activity_links}
    )
