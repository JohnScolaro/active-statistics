"""
Handle the setup of Sentry to monitor all my bugs
"""
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from active_statistics.utils.environment_variables import evm


def set_up_sentry_for_server() -> None:
    sentry_server_dsn = evm.get_sentry_server_dsn()
    if sentry_server_dsn is not None:
        sentry_sdk.init(
            dsn=sentry_server_dsn,
            integrations=[FlaskIntegration()],
            # Capture 10% of transactions for performance monitoring.
            traces_sample_rate=0.1,
        )
