"""
Instead of importing os and using os.environ everywhere with random strings,
how about I just read them all once with an "environment variable manager"
and then I can have typed access to all my variables later?
"""

import os
from typing import Any, Literal, Union, Optional

from pydantic import BaseModel, PositiveInt


class EnvironmentVariableManager:
    DOMAIN = "DOMAIN"
    PORT = "PORT"
    ENVIRONMENT = "ENVIRONMENT"
    DATA_STORAGE = "DATA_STORAGE"

    SENTRY_SERVER_DSN = "SENTRY_SERVER_DSN"
    SENTRY_WORKER_DSN = "SENTRY_WORKER_DSN"

    STRAVA_CLIENT_ID = "STRAVA_CLIENT_ID"
    STRAVA_CLIENT_SECRET = "STRAVA_CLIENT_SECRET"

    FLASK_SECRET_KEY = "FLASK_SECRET_KEY"

    ALL_VARIABLES = [
        DOMAIN,
        PORT,
        ENVIRONMENT,
        DATA_STORAGE,
        SENTRY_SERVER_DSN,
        SENTRY_WORKER_DSN,
        STRAVA_CLIENT_ID,
        STRAVA_CLIENT_SECRET,
        FLASK_SECRET_KEY,
    ]

    class ValidEnvironmentVariables(BaseModel):
        domain: str
        port: PositiveInt
        environment: Union[Literal["production"], Literal["development"]]
        data_storage: Union[Literal["local"], Literal["s3"]]
        sentry_server_dsn: Optional[str]
        sentry_worker_dsn: Optional[str]
        strava_client_id: int
        strava_client_secret: str
        flask_secret_key: str

    def __init__(self) -> None:
        # Using .get returns None for environment variables that dont exist, but that's fine because we validate them
        # with pydantic after this anyway.
        vars: dict[str, Any] = {
            variable.lower(): os.environ.get(variable)
            for variable in self.ALL_VARIABLES
        }
        self.variables = self.ValidEnvironmentVariables(**vars)

    def get_domain(self) -> str:
        return self.variables.domain

    def get_port(self) -> int:
        return self.variables.port

    def get_environment(self) -> str:
        return self.variables.environment

    def is_production(self) -> bool:
        return self.variables.environment == "production"

    def get_data_storage(self) -> str:
        return self.variables.data_storage

    def use_s3(self) -> bool:
        return self.variables.data_storage == "s3"

    def get_sentry_server_dsn(self) -> Optional[str]:
        return self.variables.sentry_server_dsn

    def get_sentry_worker_dsn(self) -> Optional[str]:
        return self.variables.sentry_worker_dsn

    def get_strava_client_id(self) -> int:
        return self.variables.strava_client_id

    def get_strava_client_secret(self) -> str:
        return self.variables.strava_client_secret

    def get_flask_secret_key(self) -> str:
        return self.variables.flask_secret_key


evm = EnvironmentVariableManager()
