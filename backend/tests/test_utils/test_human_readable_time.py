import datetime as dt

from active_statistics.utils import human_readable_time


def test_human_readable_datetime() -> None:
    assert (
        human_readable_time.datetime_to_human_readable_string(
            dt.datetime(2000, 1, 1, 12, 42, 1, 1234)
        )
        == "01/01/2000 12:42:01"
    )


def test_human_readable_timedelta() -> None:
    assert (
        human_readable_time.timedelta_to_human_readable_string(
            dt.timedelta(days=1, hours=1, minutes=1, seconds=1, microseconds=123456)
        )
        == "1 day, 1 hour, 1 minute, and 1 second"
    )
