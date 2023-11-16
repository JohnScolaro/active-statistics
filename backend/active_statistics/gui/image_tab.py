from typing import Any, Callable, Iterator

from active_statistics.gui.tabs import Tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager
from active_statistics.utils.routes import unauthorized_if_no_session_cookie
from active_statistics.utils.s3 import (
    get_captions_for_tab_images,
    get_pre_signed_urls_for_tab_images,
)
from flask import jsonify, make_response, session
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

    def get_plot_function(self) -> Callable[[Iterator[Activity], str], None]:
        return self.create_images_function

    @unauthorized_if_no_session_cookie
    def get_frontend_data(self, evm: EnvironmentVariableManager) -> Response:
        athlete_id = int(session["athlete_id"])

        response_data: list[dict[str, str]] = []

        if evm.use_s3():
            tab_images = get_pre_signed_urls_for_tab_images(athlete_id, self.get_key())

            if not tab_images:
                return make_response(
                    jsonify(
                        {
                            "key": self.get_key(),
                            "status": "Failure",
                            "tab_data": [],
                            "type": self.__class__.__name__,
                        }
                    )
                )

            try:
                tab_captions = get_captions_for_tab_images(athlete_id, self.get_key())
            except:
                return make_response(
                    jsonify(
                        {
                            "key": self.get_key(),
                            "status": "Failure",
                            "tab_data": [],
                            "type": self.__class__.__name__,
                        }
                    )
                )

            for k, v in tab_images.items():
                response_data.append({"presigned_url": v, "caption": tab_captions[k]})

        # Add the key to the response so that the frontend knows which tab the data is for.
        response_json = {
            "key": self.get_key(),
            "status": "Success",
            "tab_data": response_data,
            "type": self.__class__.__name__,
        }

        return make_response(jsonify(response_json))

    def get_type(self) -> str:
        return "plot_tab"
