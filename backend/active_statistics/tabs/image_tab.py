import json
import os
import shutil
from typing import Any, Callable, Iterator

from active_statistics.tabs.tabs import Tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager
from active_statistics.utils.local_storage import (
    get_activity_iterator,
    get_summary_activity_iterator,
)
from active_statistics.utils.s3 import (
    get_captions_for_tab_images,
    get_pre_signed_urls_for_tab_images,
    upload_file,
)
from flask import Flask, send_from_directory
from stravalib.model import Activity

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

    def get_type(self) -> str:
        return "plot_tab"

    def get_local_image_path(self) -> str:
        return os.path.join(os.getcwd(), "local_image_dir", self.get_key())

    def generate_and_register_route(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        super().generate_and_register_route(app, evm)

        def serve_image(filename: str):
            return send_from_directory(self.get_local_image_path(), filename)

        if not evm.use_s3():
            # We also want to add a dynamic route for serving locally generated images.
            app.add_url_rule(
                f"/images/{self.get_key()}/<filename>",
                f"{self.get_key()}_serve_image",
                serve_image,
            )

    def retrieve_frontend_data(
        self, evm: EnvironmentVariableManager, athlete_id: int
    ) -> Any:
        if evm.use_s3():
            tab_images = get_pre_signed_urls_for_tab_images(athlete_id, self.get_key())
            if not tab_images:
                raise Exception("No images found")
            tab_captions = get_captions_for_tab_images(athlete_id, self.get_key())

            return [
                {"url": v, "caption": tab_captions[k]} for k, v in tab_images.items()
            ]
        else:
            # Get appropriate activity iterator
            if self.is_detailed():
                activity_iterator = get_activity_iterator(athlete_id)
            else:
                activity_iterator = get_summary_activity_iterator(athlete_id)

            # Get path to local image directory, and make sure nothing is in it.
            path = self.get_local_image_path()
            if not os.path.exists(path):
                os.makedirs(path)

            if not os.listdir(path):
                # If directory is empty, recreate the images
                self.create_images_function(activity_iterator, path)

            captions_path = os.path.join(path, "captions.json")
            if os.path.exists(captions_path):
                with open(captions_path, "r") as file:
                    fp = open(captions_path)
                    captions = json.load(fp)
            else:
                captions = {}

            # These images are hosted through a dynamic route created by this tab.
            return [
                {
                    "url": f"http://{evm.get_domain()}:{evm.get_port()}/images/{self.get_key()}/{filename}",
                    "caption": captions.get(filename, "No caption found."),
                }
                for filename in os.listdir(path)
                if not filename.endswith(".json")
            ]

    def backend_processing_hook(
        self,
        activity_iterator: Iterator[Activity],
        evm: EnvironmentVariableManager,
        athlete_id: int,
    ) -> None:
        # If we are not using s3, don't do any processing. We will generate automatically when frontend is hit.
        if evm.use_s3():
            # Create a directory:
            path = self.get_local_image_path()
            if not os.path.exists(path):
                os.makedirs(path)
            try:
                # Make the images
                self.create_images_function(activity_iterator, path)
                # Add the images to an S3 bucket.
                files = os.listdir(path)
                if evm.use_s3():
                    for file in files:
                        upload_file(
                            athlete_id, self.get_key(), os.path.join(path, file)
                        )
                    # Delete the files and directory.
                    shutil.rmtree(path)
            except Exception as e:
                # Ensure that if there is an error, the tmp file gets removed anyway.
                shutil.rmtree(path)
                raise e
