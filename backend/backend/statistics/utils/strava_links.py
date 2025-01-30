from backend.tabs.table_tab import LinkCell


def get_link(url: str) -> LinkCell:
    return LinkCell(url=url, text="View on Strava")


def get_activity_url(activity_id: int) -> str:
    return f"https://www.strava.com/activities/{activity_id}"


def get_segment_url(segment_id: int) -> str:
    return f"https://www.strava.com/segments/{segment_id}"
