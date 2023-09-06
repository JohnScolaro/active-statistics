import datetime as dt
from typing import Optional

from stravalib.model import Activity

from active_statistics.trivia import TriviaProcessor, TriviaTidbitBase


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
        return f"{self.hottest_temp} Celcius"

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
        return f"{self.coldest_temp} Celcius"

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
        return f"{self.most_people} People"

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
        return f"{self.highest_max_heartrate} BPM"

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
        return f"{self.lowest_max_heartrate} BPM"

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
        return f"{self.highest_average_heartrate} BPM"

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
        return f"{self.lowest_average_heartrate} BPM"

    def get_description(self) -> str:
        return "Lowest Average Heartrate"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


class MostKudosedRunTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.activity_id: Optional[int] = None
        self.max_kudos: Optional[int] = None

    def process_activity(self, activity: Activity) -> None:
        if self.max_kudos is None or activity.kudos_count > self.max_kudos:
            self.activity_id = activity.id
            self.max_kudos = activity.kudos_count

    def get_tidbit(self) -> Optional[str]:
        return f"{self.max_kudos}"

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
        return f"{self.activity_date}"

    def get_description(self) -> str:
        return "First Activity"

    def get_activity_id(self) -> Optional[int]:
        return self.activity_id


general_trivia = TriviaProcessor()


general_trivia.register_tidbit(HottestActivityTidbit())
general_trivia.register_tidbit(ColdestActivityTidbit())
general_trivia.register_tidbit(MostPeopleOnAGroupRunTidbit())
general_trivia.register_tidbit(HighestHeartRateRecordedTidbit())
general_trivia.register_tidbit(LowestHeartRateRecordedTidbit())
general_trivia.register_tidbit(HighestAverageHeartrateTidbit())
general_trivia.register_tidbit(LowestAverageHeartrateTidbit())
general_trivia.register_tidbit(MostKudosedRunTidbit())
general_trivia.register_tidbit(FirstActivityRecordedTidbit())
