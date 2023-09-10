import datetime as dt
from typing import Optional

from stravalib.model import Activity

from active_statistics.statistics.trivia import TriviaProcessor, TriviaTidbitBase


class HottestActivityTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.hottest_temp: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if activity.average_temp is None:
            return

        if self.hottest_temp is None or self.hottest_temp < activity.average_temp:
            self.activity_id = activity.id
            self.hottest_temp = activity.average_temp

    def get_tidbit(self) -> Optional[str]:
        if self.hottest_temp:
            return f"{self.hottest_temp} Celcius"
        else:
            return None

    def get_description(self) -> str:
        return "Highest Average Temperature"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class ColdestActivityTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.coldest_temp: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if activity.average_temp is None:
            return

        if self.coldest_temp is None or self.coldest_temp > activity.average_temp:
            self.activity_id = activity.id
            self.coldest_temp = activity.average_temp

    def get_tidbit(self) -> Optional[str]:
        if self.coldest_temp:
            return f"{self.coldest_temp} Celcius"
        else:
            return None

    def get_description(self) -> str:
        return "Lowest Average Temperature"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class MostPeopleOnAGroupRunTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.most_people: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if self.most_people is None or self.most_people < activity.athlete_count:
            self.activity_id = activity.id
            self.most_people = activity.athlete_count

    def get_tidbit(self) -> Optional[str]:
        if self.most_people:
            return f"{self.most_people} People"
        else:
            return None

    def get_description(self) -> str:
        return "Most People on Group Activity"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class HighestHeartRateRecordedTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.highest_max_heartrate: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if activity.max_heartrate is None:
            return

        if (
            self.highest_max_heartrate is None
            or activity.max_heartrate > self.highest_max_heartrate
        ):
            self.activity_id = activity.id
            self.highest_max_heartrate = activity.max_heartrate

    def get_tidbit(self) -> Optional[str]:
        if self.highest_max_heartrate:
            return f"{self.highest_max_heartrate} BPM"
        else:
            return None

    def get_description(self) -> str:
        return "Highest Maximum Heartrate"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class LowestHeartRateRecordedTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.lowest_max_heartrate: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if activity.max_heartrate is None:
            return

        if (
            self.lowest_max_heartrate is None
            or activity.max_heartrate < self.lowest_max_heartrate
        ):
            self.activity_id = activity.id
            self.lowest_max_heartrate = activity.max_heartrate

    def get_tidbit(self) -> Optional[str]:
        if self.lowest_max_heartrate:
            return f"{self.lowest_max_heartrate} BPM"
        else:
            return None

    def get_description(self) -> str:
        return "Lowest Maximum Heartrate"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class HighestAverageHeartrateTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.highest_average_heartrate: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if activity.max_heartrate is None:
            return

        if (
            self.highest_average_heartrate is None
            or activity.average_heartrate > self.highest_average_heartrate
        ):
            self.activity_id = activity.id
            self.highest_average_heartrate = activity.average_heartrate

    def get_tidbit(self) -> Optional[str]:
        if self.highest_average_heartrate:
            return f"{self.highest_average_heartrate} BPM"
        else:
            return None

    def get_description(self) -> str:
        return "Highest Average Heartrate"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class LowestAverageHeartrateTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.lowest_average_heartrate: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if activity.max_heartrate is None:
            return

        if (
            self.lowest_average_heartrate is None
            or activity.average_heartrate < self.lowest_average_heartrate
        ):
            self.activity_id = activity.id
            self.lowest_average_heartrate = activity.average_heartrate

    def get_tidbit(self) -> Optional[str]:
        if self.lowest_average_heartrate:
            return f"{self.lowest_average_heartrate} BPM"
        else:
            return None

    def get_description(self) -> str:
        return "Lowest Average Heartrate"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class MostKudosedActivityTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.max_kudos: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if self.max_kudos is None or activity.kudos_count > self.max_kudos:
            self.activity_id = activity.id
            self.max_kudos = activity.kudos_count

    def get_tidbit(self) -> Optional[str]:
        if self.max_kudos:
            return f"{self.max_kudos}"
        else:
            return None

    def get_description(self) -> str:
        return "Most Kudosed Activity"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class FirstActivityRecordedTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.activity_date: Optional[dt.datetime] = None

    def process_activity(self, activity: Activity) -> None:
        if self.activity_date is None or self.activity_date > activity.start_date_local:
            self.activity_id = activity.id
            self.activity_date = activity.start_date_local

    def get_tidbit(self) -> Optional[str]:
        if self.activity_date:
            return f"{self.activity_date}"
        else:
            return None

    def get_description(self) -> str:
        return "First Activity"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class TotalKudosRecievedTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.kudos_count: int = 0

    def process_activity(self, activity: Activity) -> None:
        if activity.kudos_count is not None:
            self.kudos_count += activity.kudos_count

    def get_tidbit(self) -> Optional[str]:
        return f"{self.kudos_count}"

    def get_description(self) -> str:
        return "Total Kudos Recieved"


class EarliestActivityTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.earliest_activity_id: Optional[int] = None
        self.time_of_earliest_activity: Optional[dt.datetime] = None

    def process_activity(self, activity: Activity) -> None:
        if activity.start_date_local is not None:
            activity_time = activity.start_date_local.time()
            if (
                self.time_of_earliest_activity is None
                or activity_time <= self.time_of_earliest_activity
            ):
                self.earliest_activity_id = activity.id
                self.time_of_earliest_activity = activity_time

    def get_tidbit(self) -> Optional[str]:
        if self.time_of_earliest_activity:
            return f"{self.time_of_earliest_activity}"
        else:
            return None

    def get_description(self) -> str:
        return "Earliest Activity"

    def get_activity_id(self) -> Optional[int]:
        return self.earliest_activity_id


class LatestActivityTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.latest_activity_id: Optional[int] = None
        self.time_of_latest_activity: Optional[dt.time] = None

    def process_activity(self, activity: Activity) -> None:
        if activity.start_date_local is not None:
            activity_time = activity.start_date_local.time()
            if (
                self.time_of_latest_activity is None
                or activity_time >= self.time_of_latest_activity
            ):
                self.latest_activity_id = activity.id
                self.time_of_latest_activity = activity_time

    def get_tidbit(self) -> Optional[str]:
        if self.time_of_latest_activity:
            return f"{self.time_of_latest_activity}"
        else:
            return None

    def get_description(self) -> str:
        return "Latest Activity"

    def get_activity_id(self) -> Optional[int]:
        return self.latest_activity_id


class MostConsecutiveDaysOfActivities(TriviaTidbitBase):
    def __init__(self) -> None:
        self.date_list: list[dt.date] = []

    def process_activity(self, activity: Activity) -> None:
        if activity.start_date_local is not None:
            self.date_list.append(activity.start_date_local.date())

    def get_tidbit(self) -> Optional[str]:
        # Sort the date list in ascending order
        self.date_list.sort()

        max_consecutive_days = 1
        current_consecutive_days = 1
        start_date = self.date_list[0]
        end_date = self.date_list[0]

        # Initialize variables to track the start and end of the longest consecutive days
        max_start_date = self.date_list[0]
        max_end_date = self.date_list[0]

        for i in range(1, len(self.date_list)):
            # Calculate the difference between consecutive datetimes
            time_difference = self.date_list[i] - self.date_list[i - 1]

            # If there are multiple activities on the same day, just continue.
            if time_difference == dt.timedelta(days=0):
                continue

            # Check if the difference is one day
            if time_difference == dt.timedelta(days=1):
                current_consecutive_days += 1
                end_date = self.date_list[i]
            else:
                # If the difference is not one day, reset the current count
                current_consecutive_days = 1
                start_date = self.date_list[i]
                end_date = self.date_list[i]

            # Update the maximum consecutive days count and dates if needed
            if current_consecutive_days > max_consecutive_days:
                max_consecutive_days = current_consecutive_days
                max_start_date = start_date
                max_end_date = end_date

        return f"{max_consecutive_days} days ({max_start_date} to {max_end_date})"

    def get_description(self) -> str:
        return "Most Consecutive Days of Activities"


general_trivia = TriviaProcessor()

general_trivia.register_tidbit(HottestActivityTidbit())
general_trivia.register_tidbit(ColdestActivityTidbit())
general_trivia.register_tidbit(MostPeopleOnAGroupRunTidbit())
general_trivia.register_tidbit(HighestHeartRateRecordedTidbit())
general_trivia.register_tidbit(LowestHeartRateRecordedTidbit())
general_trivia.register_tidbit(HighestAverageHeartrateTidbit())
general_trivia.register_tidbit(LowestAverageHeartrateTidbit())
general_trivia.register_tidbit(MostKudosedActivityTidbit())
general_trivia.register_tidbit(FirstActivityRecordedTidbit())
general_trivia.register_tidbit(EarliestActivityTidbit())
general_trivia.register_tidbit(LatestActivityTidbit())
general_trivia.register_tidbit(TotalKudosRecievedTidbit())
general_trivia.register_tidbit(MostConsecutiveDaysOfActivities())
