"""
This is the only 'special' tab we have. Basically the frontend takes care of
this, all that matters is that the key it sends is hardcoded to
"download_strava_data" or whatever.
"""

from active_statistics.gui.tabs import Tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager
from flask import Flask


class DownloadStravaDataTab(Tab):
    def get_type(self) -> str:
        return self.get_key()

    def generate_and_register_routes(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        pass
