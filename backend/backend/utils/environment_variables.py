"""
Instead of importing os and using os.environ everywhere with random strings,
how about I just read them all once with an "environment variable manager"
and then I can have typed access to all my variables later?
"""

import os
from typing import Any, Literal, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, PositiveInt

# Before we do anything else, we firstly want to read the .env file and load them
# into environment variables. Using the full path works best for this because
# and running flask normally have different cwd's.
current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(current_dir, "..", "..", ".env"))


class EnvironmentVariableManager:
    PROTOCOL = "PROTOCOL"
    DOMAIN = "DOMAIN"
    FRONTEND_PORT = "FRONTEND_PORT"
    BACKEND_PORT = "BACKEND_PORT"
    ENVIRONMENT = "ENVIRONMENT"

    SENTRY_SERVER_DSN = "SENTRY_SERVER_DSN"

    STRAVA_CLIENT_ID = "STRAVA_CLIENT_ID"
    STRAVA_CLIENT_SECRET = "STRAVA_CLIENT_SECRET"

    ALL_VARIABLES = [
        PROTOCOL,
        DOMAIN,
        FRONTEND_PORT,
        BACKEND_PORT,
        ENVIRONMENT,
        SENTRY_SERVER_DSN,
        STRAVA_CLIENT_ID,
        STRAVA_CLIENT_SECRET,
    ]

    class ValidEnvironmentVariables(BaseModel):
        protocol: str
        domain: str
        frontend_port: PositiveInt
        backend_port: PositiveInt
        environment: Literal["production"] | Literal["development"]
        sentry_server_dsn: Optional[str]
        strava_client_id: int
        strava_client_secret: str

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        # Using .get returns None for environment variables that dont exist, but that's
        # fine because we validate them with pydantic after this anyway.
        vars: dict[str, Optional[str]] = {
            variable.lower(): os.environ.get(variable)
            for variable in self.ALL_VARIABLES
        }

        # If variables are passed in via kwargs, override the envvar variables.
        # This is useful for unit testing.
        kwarg_vars: dict[str, Any] = dict(kwargs.items())
        vars = vars | kwarg_vars

        self.variables = self.ValidEnvironmentVariables(**vars)  # type: ignore

    def get_protocol(self) -> str:
        return self.variables.protocol

    def get_domain(self) -> str:
        return self.variables.domain

    def get_frontend_port(self) -> int:
        return self.variables.frontend_port

    def get_backend_port(self) -> int:
        return self.variables.backend_port

    def get_environment(self) -> str:
        return self.variables.environment

    def is_production(self) -> bool:
        return self.variables.environment == "production"

    def get_sentry_server_dsn(self) -> Optional[str]:
        return self.variables.sentry_server_dsn

    def get_strava_client_id(self) -> int:
        return self.variables.strava_client_id

    def get_strava_client_secret(self) -> str:
        return self.variables.strava_client_secret


evm = EnvironmentVariableManager()
