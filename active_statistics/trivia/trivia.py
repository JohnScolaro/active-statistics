from abc import ABC, abstractmethod
from typing import Iterator, Optional

from stravalib.model import Activity


class TriviaTidbitBase(ABC):
    """
    The trivia tidbit base class. It's the job of a tidbit to give the user a
    single morsel of information. EG: "What's the segment I've ran the most
    times?" In order to not load all the activities into RAM simultaneously
    (because I'm too cheap to pay AWS for more memory) the tidbit takes each
    activity individually and saves only the information it needs to calculate
    the tidbit.
    """

    @abstractmethod
    def process_activity(self, activity: Activity) -> None:
        """
        The function that is called with each activity once, expecting this
        class to store all info required to generate the tidbit of information.
        """
        pass

    @abstractmethod
    def get_tidbit(self) -> Optional[str]:
        """
        Once all the activities have been processed, this is called to return
        the tidbit of information. This is a string like: "4.3km" or "134". Can
        be optional because we might not have a tidbit. For example, the case
        where we are trying to find the "Hottest Activity" or something, but no
        activities have temperature.
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Each tidbit has a description. Something like: "Longest Activity". Just
        some small text to explain the tidbit.
        """
        pass

    def get_activity_id(self) -> Optional[int]:
        """
        If we want to link to activities, we just implement this function which
        optionally returns the id, and we'll generate the URL from this.
        """
        return None

    def get_segment_id(self) -> Optional[int]:
        """
        If we want to link to segments, we just impliment this function, and
        the url will be generated correctly.
        """

    def get_tidbit_url(self) -> Optional[str]:
        """
        Returns the url of the tidbit. Not always required, but if the tidbit
        is something like: "Longest Run" it makes sense to link to the run so
        you can view it on Strava or something. This is that URL.
        """
        activity_id = self.get_activity_id()
        segment_id = self.get_segment_id()

        if sum(bool(optional_id) for optional_id in [activity_id, segment_id]) > 1:
            raise Exception("Only implement one id getting function.")

        if activity_id is not None:
            return f"https://www.strava.com/activities/{activity_id}"
        elif segment_id is not None:
            return f"https://www.strava.com/segments/{segment_id}"
        else:
            return None


class TriviaProcessor:
    """
    The trivia processor is processes all the individual tidbits of trivia,
    and returns them all as a list.
    """

    def __init__(self) -> None:
        self.tidbits: list[TriviaTidbitBase] = []

    def register_tidbit(self, tidbit: TriviaTidbitBase) -> None:
        self.tidbits.append(tidbit)

    def get_data(
        self, activities: Iterator[Activity]
    ) -> list[tuple[str, str, Optional[str]]]:
        trivia: list[tuple[str, str, Optional[str]]] = []

        # Process activities
        for activity in activities:
            for tidbit in self.tidbits:
                tidbit.process_activity(activity)

        # Get results
        for tidbit in self.tidbits:
            description = tidbit.get_description()
            tidbit_text = tidbit.get_tidbit()
            url = tidbit.get_tidbit_url()

            if tidbit_text is not None:
                trivia.append((description, tidbit_text, url))

        return trivia
