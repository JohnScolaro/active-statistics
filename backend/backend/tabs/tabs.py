import traceback
from abc import ABC, abstractmethod
from typing import Any, Iterator, Optional

from fastapi import FastAPI, Request
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_s3 import S3Client
from stravalib.model import DetailedActivity

from backend.utils.dynamodb import get_user_data_row_for_athlete
from backend.utils.environment_variables import EnvironmentVariableManager
from backend.utils.s3 import get_summary_activities_from_s3


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
        self,
        app: FastAPI,
        evm: EnvironmentVariableManager,
        user_table: Table,
        s3_client: S3Client,
    ) -> None:
        """
        This function is called on app startup, and registers this tabs route
        so that when the route is hit, the frontend message is returned.
        """

        async def frontend_data_retrieval_hook(request: Request) -> Any:
            session_token = request.cookies["session_token"]

            user_table_data = get_user_data_row_for_athlete(user_table, session_token)
            summary_activities = get_summary_activities_from_s3(
                s3_client, user_table_data.athlete_id
            )

            response_msg = {"key": self.get_key(), "type": self.__class__.__name__}

            try:
                frontend_data = self.generate_and_return_tab_data(
                    summary_activities, evm, user_table_data.athlete_id
                )
                response_msg["status"] = "Success"
                response_msg["tab_data"] = frontend_data

            except Exception as e:
                print(e)
                traceback.print_exc()
                response_msg["status"] = "Failure"

            return response_msg

        frontend_data_retrieval_hook.__name__ = f"{self.get_key()}"
        app.add_api_route(
            path=f"/api/data/{self.get_key()}",
            endpoint=frontend_data_retrieval_hook,
            methods=["GET"],
        )

    @abstractmethod
    def generate_and_return_tab_data(
        self,
        activity_iterator: Iterator[DetailedActivity],
        evm: EnvironmentVariableManager,
        athlete_id: int,
    ) -> Any:
        """
        Function to implement for each tab. Takes the list of all detailed activities,
        and returns the required data for the tab to display.
        """
        pass
