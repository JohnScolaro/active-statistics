import json
from typing import Any, Callable, Iterator, Optional

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

from active_statistics.gui.tabs import Tab
from active_statistics.trivia import TriviaProcessor
from active_statistics.utils.environment_variables import EnvironmentVariableManager
from active_statistics.utils.local_storage import (
    get_activity_iterator,
    get_summary_activity_iterator,
)
from active_statistics.utils.s3 import get_plot_data


class TriviaTab(Tab):
    def __init__(
        self,
        name: str,
        detailed: bool,
        description: str,
        trivia_processor: TriviaProcessor,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, detailed, **kwargs)
        self.description = description
        self.trivia_processor = trivia_processor

    def generate_and_register_routes(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        self.generate_and_register_page_function(app, evm)
        self.generate_and_register_data_function(app, evm)

    def generate_and_register_page_function(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        # These functions generate the view functions we need for each route.
        def get_page_function(tab: TriviaTab) -> Callable[[], Response]:
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
        def get_data_function(tab: TriviaTab):
            def data_function() -> Response:
                if "athlete_id" not in session:
                    return redirect(url_for("index"))

                athlete_id = int(session["athlete_id"])

                if evm.use_s3():
                    trivia_data_str = get_plot_data(athlete_id, tab.get_key())

                    # If there is no data in S3 for this key, return a blank figure.
                    trivia_data: list[tuple[str, str, Optional[str]]]
                    if trivia_data_str is None:
                        trivia_data = []
                    else:
                        trivia_data = json.loads(trivia_data_str)
                else:
                    activity_iterator: Iterator[Activity]
                    if tab.is_detailed():
                        activity_iterator = get_activity_iterator(athlete_id)
                    else:
                        activity_iterator = get_summary_activity_iterator(athlete_id)

                    trivia_data = self.trivia_processor.get_data(activity_iterator)

                # Add the key to the response so that the frontend knows which tab the data is for.
                response_json = {"key": tab.get_key(), "chart_json": trivia_data}

                return make_response(jsonify(response_json))

            data_function.__name__ = f"{tab.get_key()}_data"
            return data_function

        app.add_url_rule(self.get_data_endpoint(), view_func=get_data_function(self))

    def get_data_endpoint(self) -> str:
        return f"/data/{self.get_key()}"

    def get_main_content(self) -> str:
        return render_template(
            "trivia_tab_main_content_container.html",
            explanation=self.description,
            trivia_endpoint=self.get_data_endpoint(),
            key=self.get_key(),
        )
