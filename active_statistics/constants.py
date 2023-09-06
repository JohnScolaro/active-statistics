import datetime as dt

# Data timeout
DATA_TIMEOUT: dt.timedelta = dt.timedelta(days=7)
DATA_TIMEOUT_SECONDS: int = int(DATA_TIMEOUT.total_seconds())
