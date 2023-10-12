import dataclasses
from typing import Union

from active_statistics.gui.tabs import Tab


@dataclasses.dataclass
class TabGroup:
    name: str
    key: str
    children: list[Union[Tab, "TabGroup"]]

    def get_key(self):
        return ""

    def get_type(self):
        return ""
