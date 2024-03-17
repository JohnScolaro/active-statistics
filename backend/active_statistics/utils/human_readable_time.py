"""
Just a helper to convert datetimes and timedeltas to strings that are easier on the eyes.
"""

import datetime as dt


def datetime_to_human_readable_string(datetime: dt.datetime) -> str:
    return datetime.strftime("%d/%m/%Y %H:%M:%S")


def timedelta_to_human_readable_string(timedelta: dt.timedelta) -> str:
    return (
        f"{timedelta.days} day{'' if timedelta.days == 1 else 's'}, "
        f"{timedelta.seconds // 3600} hour{'' if timedelta.seconds//3600 == 1 else 's'}, "
        f"{(timedelta.seconds // 60) % 60} minute{'' if (timedelta.seconds // 60) % 60== 1 else 's'}, "
        f"and {timedelta.seconds % 60} second{'' if timedelta.seconds % 60 == 1 else 's'}"
    )
