import json
from typing import Any, Callable, Iterator

import plotly
from stravalib.model import DetailedActivity

from backend.tabs.tabs import Tab
from backend.utils.environment_variables import EnvironmentVariableManager


class AnimatedPolylineGridTab(Tab):
    def __init__(
        self,
        name: str,
        detailed: bool,
        description: str,
        create_images_function: Callable[[Iterator[DetailedActivity], str], None],
        **kwargs: Any,
    ) -> None:
        super().__init__(name, detailed, **kwargs)
        self.description = description
        self.create_images_function = create_images_function

    def get_plot_function(self) -> Callable[[Iterator[DetailedActivity], str], None]:
        return self.create_images_function

    def get_type(self) -> str:
        return "animated_polyline_grid_tab"

    def generate_and_return_tab_data(
        self,
        activity_iterator: Iterator[DetailedActivity],
        evm: EnvironmentVariableManager,
        athlete_id: int,
    ) -> None:
        """
        The images are made in a canvas on the frontend, so just send them the data that
        they need, and they'll take care of the rest.
        """
        return json.loads(
            json.dumps(
                [
                    {
                        "start_datetime": activity.start_date_local,
                        "polyline": activity.map.summary_polyline,
                        "type": activity.type.root,
                    }
                    for activity in activity_iterator
                    if activity.map.summary_polyline != ""
                ],
                cls=plotly.utils.PlotlyJSONEncoder,
            )
        )
