import json
from typing import Any, Callable, Iterator, Optional

import pandas as pd
from active_statistics.gui.tabs import Tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager
from active_statistics.utils.local_storage import (
    get_activity_iterator,
    get_summary_activity_iterator,
)
from active_statistics.utils.s3 import get_visualisation_data
from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    session,
    url_for,
)
from stravalib.model import Activity
from werkzeug.wrappers import Response


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
        self.generate_and_register_page_function(app, evm)
        self.generate_and_register_data_function(app, evm)

    def get_table_dataframe(self, activities: Iterator[Activity]) -> pd.DataFrame:
        if self.table_function is None:
            raise Exception("Table tab has no function to generate a table.")
        return self.table_function(activities)

    def has_column_headings(self):
        return True

    def get_table_data(self, activities: Iterator[Activity]) -> dict[str, Any]:
        df = self.get_table_dataframe(activities)
        return {
            "table_data": df.to_dict(orient="list"),
            "show_headings": self.has_column_headings(),
            "heading_order": list(df.columns),
        }

    def generate_and_register_page_function(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        # These functions generate the view functions we need for each route.
        def get_page_function(tab: TableTab) -> Callable[[], Response]:
            def page_function() -> Response:
                if "athlete_id" not in session:
                    return redirect(url_for("index"))

                return make_response(tab.get_main_content())

            page_function.__name__ = f"{tab.get_key()}_page"
            return page_function

        app.add_url_rule(self.get_page_endpoint(), view_func=get_page_function(self))

    def generate_and_register_data_function(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        def get_data_function(tab: TableTab):
            def data_function() -> Response:
                if "athlete_id" not in session:
                    return redirect(url_for("index"))

                athlete_id = int(session["athlete_id"])

                if evm.use_s3():
                    table_data_str = get_visualisation_data(athlete_id, tab.get_key())

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
                response_json = {"key": tab.get_key(), "chart_json": table_data}

                return make_response(jsonify(response_json))

            data_function.__name__ = f"{tab.get_key()}_data"
            return data_function

        app.add_url_rule(self.get_data_endpoint(), view_func=get_data_function(self))

    def get_data_endpoint(self) -> str:
        return f"/data/{self.get_key()}"

    def get_main_content(self) -> str:
        return render_template(
            "table_tab_main_content_container.html",
            explanation=self.description,
            table_endpoint=self.get_data_endpoint(),
            key=self.get_key(),
        )
