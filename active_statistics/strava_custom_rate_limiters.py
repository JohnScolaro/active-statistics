from stravalib.util.limiter import RateLimiter, XRateLimitRule


class DetailedTaskRateLimiter(RateLimiter):
    """
    A custom rate limiter. Limits api calls to 150 (instead of default 200) per 15 minutes, and 1,000 instead of
    default 2,000 per day. This should leave some more room for auth calls for users, and not just use up my whole
    bandwidth downloading detailed data for a few users.
    """

    def __init__(self):
        super(DetailedTaskRateLimiter, self).__init__()
        self.rules.append(
            XRateLimitRule(
                {
                    "short": {
                        "usageFieldIndex": 0,
                        "usage": 0,
                        "limit": 200,
                        # 60s * 15 = 15 min
                        "time": (60 * 15),
                        "lastExceeded": None,
                    },
                    "long": {
                        "usageFieldIndex": 1,
                        "usage": 0,
                        "limit": 1000,
                        # 60s * 60m * 24 = 1 day
                        "time": (60 * 60 * 24),
                        "lastExceeded": None,
                    },
                }
            )
        )
