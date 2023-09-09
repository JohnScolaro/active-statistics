def get_activity_url(activity_id: int) -> str:
    return f"https://www.strava.com/activities/{activity_id}"


def get_segment_url(segment_id: int) -> str:
    return f"https://www.strava.com/segments/{segment_id}"


def get_html_link(url: str) -> str:
    return f'<a href="{url}">View on Strava</a>'
