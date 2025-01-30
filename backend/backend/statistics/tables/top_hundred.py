"""
The idea is that this is a generic "top 100's" table creator for all Strava
activities. I can simply say I want "a table of the top 100 longest runs" or
"shortest runs" or "most kudosed" or "hottest" activities or whatever, and this
code can handle getting that data, and displaying it later in a table.
"""

from typing import Any, Callable, Iterator

import pandas as pd
from stravalib import unit_helper as uh
from stravalib.model import ActivityType, DetailedActivity

from backend.statistics.utils.strava_links import get_activity_url, get_link


def get_top_hundred_table_function(
    activity_type: ActivityType,
    attribute_name: str,
    attribute_column_name: str,
    attribute_conversion_function: Callable[[Any], Any],
) -> Callable[[Iterator[DetailedActivity]], pd.DataFrame]:
    def top_hundred_table_function(
        activities: Iterator[DetailedActivity],
    ) -> pd.DataFrame:
        activity_names = []
        attribute_column = []
        activity_links = []

        for activity in activities:
            if activity.type.root == activity_type:
                activity_names.append(activity.name)
                attribute_column.append(
                    attribute_conversion_function(getattr(activity, attribute_name))
                )
                activity_links.append(get_link(get_activity_url(activity.id)))

        # Create a DataFrame with the specified attribute as a column
        data = {
            "Activity Name": activity_names,
            attribute_column_name: attribute_column,
            "Activity Link": activity_links,
        }
        df = pd.DataFrame(data)

        # Sort the df
        df = df.sort_values(by=[attribute_column_name], ascending=False)

        # Only keep top 100
        df = df.head(100)

        # Add a rank column as the first column
        df.insert(0, "Rank", df.reset_index().index + 1)

        # Shorten the values
        df[attribute_column_name] = df[attribute_column_name].apply(
            lambda x: f"{x:.2f}"
        )

        return df

    return top_hundred_table_function


def distance_conversion_function_to_km(quantity: uh._Quantity) -> float:
    return uh.kilometers(quantity).magnitude
