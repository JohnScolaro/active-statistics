from abc import ABC, abstractmethod
from typing import Optional

from active_statistics.utils.environment_variables import EnvironmentVariableManager
from flask import Flask
from werkzeug.wrappers import Response


class Tab(ABC):
    def __init__(self, name: str, detailed: bool, key: Optional[str] = None) -> None:
        self.name = name
        self.detailed = detailed
        self.key = key

    def get_name(self) -> str:
        return self.name

    def get_key(self) -> str:
        if self.key is None:
            # I can't be bothered using slugify.
            return self.name.lower().replace(" ", "_")
        else:
            return self.key

    def generate_and_register_route(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        """
        This function is called on app startup, and registers this tabs route
        so that when the route is hit, the frontend message is returned.
        """

        def frontend_message_handler() -> Response:
            return self.get_frontend_data(evm)

        frontend_message_handler.__name__ = f"{self.get_key()}"
        app.add_url_rule(
            f"/api/data/{self.get_key()}", view_func=frontend_message_handler
        )

    @abstractmethod
    def get_frontend_data(self, evm: EnvironmentVariableManager) -> Response:
        pass

    def is_detailed(self) -> bool:
        return self.detailed

    @abstractmethod
    def get_type(self) -> str:
        pass
