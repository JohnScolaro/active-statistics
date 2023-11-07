import dataclasses
import json
from typing import Any, Callable, Iterator, Literal, Optional

import pandas as pd
from active_statistics.gui.tabs import Tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager
from active_statistics.utils.local_storage import (
    get_activity_iterator,
    get_summary_activity_iterator,
)
from active_statistics.utils.routes import unauthorized_if_no_session_cookie
from active_statistics.utils.s3 import get_tab_data
from flask import Flask, jsonify, make_response, session
from stravalib.model import Activity
from werkzeug.wrappers import Response

ColumnTypes = Literal["string", "link"]


@dataclasses.dataclass
class LinkCell:
    url: str
    text: str


class TableTab(Tab):
    def __init__(
        self,
        name: str,
        detailed: bool,
        description: str,
        table_function: Optional[Callable[[Iterator[Activity]], pd.DataFrame]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, detailed, **kwargs)
        self.description = description
        self.table_function = table_function

    def generate_and_register_routes(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        def get_data_function(tab: TableTab):
            @unauthorized_if_no_session_cookie
            def data_function() -> Response:
                athlete_id = int(session["athlete_id"])

                if evm.use_s3():
                    table_data_str = get_tab_data(athlete_id, tab.get_key())

                    # If there is no data in S3 for this key, return a blank figure.
                    table_data: dict[Any, Any]
                    if table_data_str is None:
                        table_data = {}
                    else:
                        table_data = json.loads(table_data_str)
                else:
                    activity_iterator: Iterator[Activity]
                    if tab.is_detailed():
                        activity_iterator = get_activity_iterator(athlete_id)
                    else:
                        activity_iterator = get_summary_activity_iterator(athlete_id)

                    table_data = self.get_table_data(activity_iterator)

                # Add the key to the response so that the frontend knows which tab the data is for.
                response_json = {
                    "key": tab.get_key(),
                    "tab_data": table_data,
                    "type": self.__class__.__name__,
                }

                return make_response(jsonify(response_json))

            data_function.__name__ = f"{tab.get_key()}_data"
            return data_function

        app.add_url_rule(self.get_data_endpoint(), view_func=get_data_function(self))

    def get_table_dataframe(self, activities: Iterator[Activity]) -> pd.DataFrame:
        if self.table_function is None:
            raise Exception("Table tab has no function to generate a table.")
        return self.table_function(activities)

    def get_table_column_types(self) -> dict[str, ColumnTypes]:
        return {}

    def has_column_headings(self):
        return True

    def get_columns(self, df: pd.DataFrame) -> list[dict[str, str]]:
        column_types = self.get_table_column_types()
        return [
            {"column_name": col, "column_type": column_types.get(col, "string")}
            for col in df.columns
        ]

    def get_table_data(self, activities: Iterator[Activity]) -> dict[str, Any]:
        df = self.get_table_dataframe(activities)

        def serialise_linkcells(
            linkcell: Optional[LinkCell],
        ) -> Optional[dict[str, Any]]:
            if linkcell is not None:
                return dataclasses.asdict(linkcell)
            else:
                return None

        column_types = self.get_table_column_types()
        for col in df.columns:
            if column_types.get(col, "string") == "link":
                df[col] = df[col].apply(serialise_linkcells)

        return {
            "table_data": df.to_dict(orient="list"),
            "show_headings": self.has_column_headings(),
            "columns": self.get_columns(df),
        }

    def get_data_endpoint(self) -> str:
        return f"/api/data/{self.get_key()}"

    def get_type(self) -> str:
        return "table_tab"
