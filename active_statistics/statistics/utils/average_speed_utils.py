"""
When you're working with a graph with "average speed" on the y-axis, you tend to want different units for different
activity types. Here are all my utils for converting between them.
"""

import dataclasses
import datetime as dt
import math
from typing import Callable, Optional, Union

from stravalib import unithelper as uh
from stravalib.model import ActivityType


def average_speed_to_kmph(average_speed_in_m_per_sec: uh.Quantity) -> Optional[float]:
    if math.isnan(average_speed_in_m_per_sec):
        return None
    else:
        return float(average_speed_in_m_per_sec.magnitude / 1000 * 3600)


def average_speed_to_mins_per_km(
    average_speed_in_m_per_sec: uh.Quantity,
) -> Optional[dt.datetime]:
    """
    Plotly doesn't support timedelta on the y-axis, so we show datetimes, and just change the plot formatting to make
    it look correct.
    """
    # If the speed is 0, then the mins/km would be infinity and ruin the plot, so just return None in this case.
    if average_speed_in_m_per_sec.magnitude == 0:
        return None

    if math.isnan(average_speed_in_m_per_sec):
        return None
    else:
        return dt.datetime(1970, 1, 1) + dt.timedelta(
            seconds=int(1000 / average_speed_in_m_per_sec.magnitude)
        )


@dataclasses.dataclass
class AverageSpeedYAxisSettings:
    conversion_function: Callable[[uh.Quantity], Union[None, float, dt.datetime]]
    tick_format: Optional[str]
    axis_title: str


ACTIVITY_TO_Y_AXIS_SETTINGS_MAPPING: dict[ActivityType, AverageSpeedYAxisSettings] = {
    "AlpineSki": AverageSpeedYAxisSettings(
        conversion_function=average_speed_to_kmph,
        tick_format=None,
        axis_title="Average Pace (kmph)",
    ),
    "Ride": AverageSpeedYAxisSettings(
        conversion_function=average_speed_to_kmph,
        tick_format=None,
        axis_title="Average Pace (kmph)",
    ),
    "Run": AverageSpeedYAxisSettings(
        conversion_function=average_speed_to_mins_per_km,
        tick_format="%M:%S",
        axis_title="Average Pace (mins/km)",
    ),
    "Walk": AverageSpeedYAxisSettings(
        conversion_function=average_speed_to_mins_per_km,
        tick_format="%M:%S",
        axis_title="Average Pace (mins/km)",
    ),
}


def get_y_axis_settings(activity_type: ActivityType) -> AverageSpeedYAxisSettings:
    return ACTIVITY_TO_Y_AXIS_SETTINGS_MAPPING.get(
        activity_type,
        AverageSpeedYAxisSettings(
            conversion_function=average_speed_to_kmph,
            tick_format=None,
            axis_title="Average Pace (kmph)",
        ),
    )
