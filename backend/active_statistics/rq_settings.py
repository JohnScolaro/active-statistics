import sentry_sdk
from active_statistics.utils.environment_variables import evm
from sentry_sdk.integrations.rq import RqIntegration

if evm.is_production():
    sentry_worker_dsn = evm.get_sentry_worker_dsn()
    if sentry_worker_dsn is not None:
        sentry_sdk.init(
            dsn=sentry_worker_dsn,
            integrations=[
                RqIntegration(),
            ],
            # Capture 10% of transactions for performance monitoring.
            traces_sample_rate=0.1,
        )
