from typing import Optional

from flask import Flask

from active_statistics.utils.environment_variables import EnvironmentVariableManager


class Tab:
    def __init__(self, name: str, detailed: bool, key: Optional[str] = None) -> None:
        self.name = name
        self.detailed = detailed
        self.key = key

    def get_name(self) -> str:
        return self.name

    def get_key(self) -> str:
        if self.key is None:
            # I can't be bothered using slugify.
            return self.name.lower().replace(" ", "_")
        else:
            return self.key

    def get_page_endpoint(self) -> str:
        return f"/page/{self.get_key()}"

    def generate_and_register_routes(
        self, app: Flask, evm: EnvironmentVariableManager
    ) -> None:
        """
        This is a hefty function that is called on app startup, where the
        server loops though all tabs and creates the routes required for them.
        """
        raise NotImplementedError()

    def is_detailed(self) -> bool:
        return self.detailed
