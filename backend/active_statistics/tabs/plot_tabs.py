import json
from typing import Any, Callable, Iterator

import plotly
import plotly.graph_objects as go
from active_statistics.tabs.tabs import Tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager
from active_statistics.utils.local_storage import (
    get_activity_iterator,
    get_summary_activity_iterator,
)
from active_statistics.utils.s3 import get_object, save_chart_json
from stravalib.model import Activity


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

    def get_plot_function(self) -> Callable[[Iterator[Activity]], go.Figure]:
        return self.plot_function

    def retrieve_frontend_data(
        self, evm: EnvironmentVariableManager, athlete_id: int
    ) -> Any:
        # If we are using S3, just get the pre-processed chart data from s3,
        # otherwise process it here and return it.
        if evm.use_s3():
            chart_string = get_object(athlete_id, self.get_key(), "chart.json")
            return json.loads(chart_string)
        else:
            # If we aren't using s3, get the activity iterator here, because
            # all the data should be pre-downloaded.
            if self.is_detailed():
                activity_iterator = get_activity_iterator(athlete_id)
            else:
                activity_iterator = get_summary_activity_iterator(athlete_id)

            return self.get_chart_dict(activity_iterator)

    def backend_processing_hook(
        self,
        activity_iterator: Iterator[Activity],
        evm: EnvironmentVariableManager,
        athlete_id: int,
    ) -> None:
        # If we aren't using S3, just do nothing because it'll all happen on the frontend data retrieval hook.
        if evm.use_s3():
            chart_data = self.get_chart_dict(activity_iterator)
            chart_json_string = json.dumps(
                chart_data, cls=plotly.utils.PlotlyJSONEncoder
            )
            save_chart_json(athlete_id, self.get_key(), chart_json_string)

    def get_chart_dict(self, activity_iterator: Iterator[Activity]) -> Any:
        fig = self.plot_function(activity_iterator)

        # Convert the chart figure to a dictionary which can be correctly serialised by flasks `jsonify`.
        # We can't just rely on jsonify, because it serialised datetimes incorrectly, so we use plotlys
        # json encoder to make a string, then read that back into a dictionary. This serialises all the
        # datetimes correctly.
        chart_json_string = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        chart_dict = json.loads(chart_json_string)
        return chart_dict

    def get_type(self) -> str:
        return "plot_tab"
