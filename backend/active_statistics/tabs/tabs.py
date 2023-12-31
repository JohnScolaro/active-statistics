from abc import ABC, abstractmethod
from typing import Any, Iterator, Optional

from active_statistics.utils.environment_variables import EnvironmentVariableManager
from active_statistics.utils.routes import unauthorized_if_no_session_cookie
from flask import Flask, jsonify, make_response, session
from stravalib.model import Activity
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

    def is_detailed(self) -> bool:
        return self.detailed

    @abstractmethod
    def get_type(self) -> str:
        pass

    def generate_and_register_route(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        """
        This function is called on app startup, and registers this tabs route
        so that when the route is hit, the frontend message is returned.
        """

        @unauthorized_if_no_session_cookie
        def frontend_data_retrieval_hook() -> Response:
            athlete_id = int(session["athlete_id"])

            response_msg = {"key": self.get_key(), "type": self.__class__.__name__}

            try:
                frontend_data = self.retrieve_frontend_data(evm, athlete_id)
                response_msg["status"] = "Success"
                response_msg["tab_data"] = frontend_data

            except Exception as e:
                print(e)
                response_msg["status"] = "Failure"

            return make_response(jsonify(response_msg))

        frontend_data_retrieval_hook.__name__ = f"{self.get_key()}"
        app.add_url_rule(
            f"/api/data/{self.get_key()}", view_func=frontend_data_retrieval_hook
        )

    @abstractmethod
    def retrieve_frontend_data(
        self, evm: EnvironmentVariableManager, athlete_id: int
    ) -> Any:
        pass

    @abstractmethod
    def backend_processing_hook(
        self,
        activity_iterator: Iterator[Activity],
        evm: EnvironmentVariableManager,
        athlete_id: int,
    ) -> None:
        """
        This is the backend processing hook for the tab. It is called when the
        rq worker attempts to do any preprocessing for the tab.
        """
        pass
