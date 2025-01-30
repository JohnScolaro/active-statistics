from typing import Iterator

import pandas as pd
from stravalib.model import DetailedActivity

from backend.statistics.utils.strava_links import get_activity_url, get_link


def flagged_activities_table(activities: Iterator[DetailedActivity]) -> pd.DataFrame:
    flagged_activities = [activity for activity in activities if activity.flagged]

    activity_names = [activity.name for activity in flagged_activities]
    activity_links = [
        get_link(get_activity_url(activity.id)) for activity in flagged_activities
    ]

    return pd.DataFrame(
        {"Activity Names": activity_names, "Activity Links": activity_links}
    )
