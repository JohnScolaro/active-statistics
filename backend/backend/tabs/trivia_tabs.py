from typing import Any, Iterator

import pandas as pd
from stravalib.model import DetailedActivity

from backend.statistics.trivia import TriviaProcessor
from backend.tabs.table_tab import TableTab


class TriviaTab(TableTab):
    def __init__(
        self,
        name: str,
        detailed: bool,
        description: str,
        trivia_processor: TriviaProcessor,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, detailed, description, **kwargs)
        self.description = description
        self.trivia_processor = trivia_processor

    def get_table_dataframe(
        self, activities: Iterator[DetailedActivity]
    ) -> pd.DataFrame:
        trivia_data = self.trivia_processor.get_data(activities)

        descriptions = []
        tidbit_info = []
        optional_links = []
        for description, tidbit, link in trivia_data:
            descriptions.append(description)
            tidbit_info.append(tidbit)
            optional_links.append(link)

        return pd.DataFrame(
            {
                "tidbit_description": descriptions,
                "tidbit_info": tidbit_info,
                "optional_link": optional_links,
            }
        )

    def get_table_column_types(self):
        return {
            "tidbit_description": "string",
            "tidbit_info": "string",
            "optional_link": "link",
        }

    def has_column_headings(self):
        return False
