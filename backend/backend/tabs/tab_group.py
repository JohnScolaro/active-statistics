import dataclasses
from typing import Union

from backend.tabs.tabs import Tab


@dataclasses.dataclass
class TabGroup:
    name: str
    key: str
    children: list[Union[Tab, "TabGroup"]]

    def get_key(self) -> str:
        # I can't be bothered using slugify.
        return self.name.lower().replace(" ", "_")

    def get_type(self):
        return ""
