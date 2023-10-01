import json
from typing import Any, Callable, Iterator

import plotly
import plotly.graph_objects as go
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


class PlotTab(Tab):
    def __init__(
        self,
        name: str,
        detailed: bool,
        description: str,
        plot_function: Callable[[Iterator[Activity]], go.Figure],
        **kwargs: Any,
    ) -> None:
        super().__init__(name, detailed, **kwargs)
        self.description = description
        self.plot_function = plot_function

    def get_main_content(self) -> str:
        return render_template(
            "plot_tab_main_content_container.html",
            explanation=self.description,
            plot_endpoint=self.get_plot_endpoint(),
            key=self.get_key(),
        )

    def get_plot_endpoint(self) -> str:
        return f"/plot/{self.get_key()}"

    def get_plot_function(self) -> Callable[[Iterator[Activity]], go.Figure]:
        return self.plot_function

    def generate_and_register_routes(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        self.generate_and_register_page_function(app, evm)
        self.generate_and_register_plot_function(app, evm)

    def generate_and_register_page_function(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        # These functions generate the view functions we need for each route.
        def get_page_function(tab: PlotTab) -> Callable[[], Response]:
            def page_function() -> Response:
                if "athlete_id" not in session:
                    return redirect(url_for("index"))

                return make_response(tab.get_main_content())

            page_function.__name__ = f"{tab.get_key()}_page"
            return page_function

        app.add_url_rule(self.get_page_endpoint(), view_func=get_page_function(self))

    def generate_and_register_plot_function(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        def get_plot_function(tab: PlotTab):
            def plot_function() -> Response:
                if "athlete_id" not in session:
                    return redirect(url_for("index"))

                athlete_id = int(session["athlete_id"])

                if evm.use_s3():
                    chart_json_string = get_visualisation_data(
                        athlete_id, tab.get_key()
                    )

                    # If there is no chart data in S3 for this chart, return a blank figure.
                    if chart_json_string is None:
                        chart_dict = {}
                    else:
                        chart_dict = json.loads(chart_json_string)
                else:
                    activity_iterator: Iterator[Activity]
                    if tab.is_detailed():
                        activity_iterator = get_activity_iterator(athlete_id)
                    else:
                        activity_iterator = get_summary_activity_iterator(athlete_id)
                    fig: go.Figure = tab.plot_function(activity_iterator)

                    # Convert the chart figure to a dictionary which can be correctly serialised by flasks `jsonify`.
                    # We can't just rely on jsonify, because it serialised datetimes incorrectly, so we use plotlys
                    # json encoder to make a string, then read that back into a dictionary. This serialises all the
                    # datetimes correctly.
                    chart_json_string = json.dumps(
                        fig, cls=plotly.utils.PlotlyJSONEncoder
                    )
                    chart_dict = json.loads(chart_json_string)

                # Add the key to the response so that the frontend knows which tab the data is for.
                response_json = {"key": tab.get_key(), "chart_json": chart_dict}

                return make_response(jsonify(response_json))

            plot_function.__name__ = f"{tab.get_key()}_plot"
            return plot_function

        app.add_url_rule(self.get_plot_endpoint(), view_func=get_plot_function(self))
