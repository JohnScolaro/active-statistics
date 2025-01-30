import json
from typing import Any, Callable, Iterator

import plotly
import plotly.graph_objects as go
from stravalib.model import DetailedActivity

from backend.tabs.tabs import Tab
from backend.utils.environment_variables import EnvironmentVariableManager


class PlotTab(Tab):
    def __init__(
        self,
        name: str,
        detailed: bool,
        description: str,
        plot_function: Callable[[Iterator[DetailedActivity]], go.Figure],
        **kwargs: Any,
    ) -> None:
        super().__init__(name, detailed, **kwargs)
        self.description = description
        self.plot_function = plot_function

    def get_plot_function(self) -> Callable[[Iterator[DetailedActivity]], go.Figure]:
        return self.plot_function

    def generate_and_return_tab_data(
        self,
        activity_iterator: Iterator[DetailedActivity],
        evm: EnvironmentVariableManager,
        athlete_id: int,
    ) -> None:
        fig = self.plot_function(activity_iterator)
        chart_json_string = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return json.loads(chart_json_string)

    def get_type(self) -> str:
        return "plot_tab"
