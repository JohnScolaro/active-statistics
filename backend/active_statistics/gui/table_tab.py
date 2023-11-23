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
from active_statistics.utils.s3 import get_object, save_table_json
from flask import jsonify, make_response, session
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

    def get_type(self) -> str:
        return "table_tab"

    def retrieve_frontend_data(
        self, evm: EnvironmentVariableManager, athlete_id: int
    ) -> Any:
        if evm.use_s3():
            table_string = get_object(athlete_id, self.get_key(), "table.json")
            return json.loads(table_string)
        else:
            # If we aren't using s3, get the activity iterator here, because
            # all the data should be pre-downloaded.
            if self.is_detailed():
                activity_iterator = get_activity_iterator(athlete_id)
            else:
                activity_iterator = get_summary_activity_iterator(athlete_id)
            return self.get_table_data(activity_iterator)

    def backend_processing_hook(
        self,
        activity_iterator: Iterator[Activity],
        evm: EnvironmentVariableManager,
        athlete_id: int,
    ) -> None:
        # If we aren't using S3, just leave it for the frontend hook to generate.
        if evm.use_s3():
            table_data = self.get_table_data(activity_iterator)
            table_json_string = json.dumps(table_data)
            save_table_json(athlete_id, self.get_key(), table_json_string)
