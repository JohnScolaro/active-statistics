import dataclasses
from typing import Union

from active_statistics.gui.tabs import Tab


@dataclasses.dataclass
class TabGroup:
    name: str
    key: str
    children: list[Union[Tab, "TabGroup"]]

    def get_key(self) -> str:
        if self.key is None:
            # I can't be bothered using slugify.
            return self.name.lower().replace(" ", "_")
        else:
            return self.key

    def get_type(self):
        return ""
