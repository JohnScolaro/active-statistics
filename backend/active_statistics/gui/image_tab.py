from typing import Any, Callable, Iterator

from active_statistics.gui.tabs import Tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager
from active_statistics.utils.routes import unauthorized_if_no_session_cookie
from active_statistics.utils.s3 import get_tab_images
from flask import Flask, jsonify, make_response, session
from stravalib.model import Activity
from werkzeug.wrappers import Response

Image = Any


class ImageTab(Tab):
    def __init__(
        self,
        name: str,
        detailed: bool,
        description: str,
        create_images_function: Callable[[Iterator[Activity], str], None],
        **kwargs: Any,
    ) -> None:
        super().__init__(name, detailed, **kwargs)
        self.description = description
        self.create_images_function = create_images_function

    def get_plot_endpoint(self) -> str:
        return f"/api/data/{self.get_key()}"

    def get_plot_function(self) -> Callable[[Iterator[Activity]], list[Image]]:
        return self.plot_function

    def generate_and_register_routes(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        def get_plot_function(tab: ImageTab):
            @unauthorized_if_no_session_cookie
            def plot_function() -> Response:
                athlete_id = int(session["athlete_id"])

                if evm.use_s3():
                    tab_images = get_tab_images(athlete_id, tab.get_key())
                else:
                    tab_images = []

                # Add the key to the response so that the frontend knows which tab the data is for.
                response_json = {
                    "key": tab.get_key(),
                    "tab_data": tab_images,
                    "type": self.__class__.__name__,
                }

                return make_response(jsonify(response_json))

            plot_function.__name__ = f"{tab.get_key()}_plot"
            return plot_function

        app.add_url_rule(self.get_plot_endpoint(), view_func=get_plot_function(self))

    def get_type(self) -> str:
        return "plot_tab"
