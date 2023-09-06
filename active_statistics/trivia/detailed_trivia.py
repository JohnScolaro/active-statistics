from collections import Counter
from typing import Optional

from stravalib.model import Activity

from active_statistics.trivia import TriviaProcessor, TriviaTidbitBase


class TotalNumberOfSegmentsTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.segment_count = 0

    def process_activity(self, activity: Activity) -> None:
        self.segment_count += len(activity.segment_efforts)

    def get_description(self) -> str:
        return "Total Number of Segments Completed"

    def get_tidbit(self) -> Optional[str]:
        return str(self.segment_count)


class TotalUniqueSegmentsTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.segment_counter: Counter[int] = Counter()

    def process_activity(self, activity: Activity) -> None:
        self.segment_counter.update(
            segment_effort.segment.id for segment_effort in activity.segment_efforts
        )

    def get_description(self) -> str:
        return "Total Unique Segments Completed"

    def get_tidbit(self) -> Optional[str]:
        return str(len(self.segment_counter))


class MostRanSegmentTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.segment_counter: Counter[int] = Counter()

    def process_activity(self, activity: Activity) -> None:
        self.segment_counter.update(
            segment_effort.segment.id for segment_effort in activity.segment_efforts
        )

    def get_description(self) -> str:
        return "Most Popular Segment"

    def get_tidbit(self) -> Optional[str]:
        return f"{self.segment_counter.most_common(1)[0][1]} completions"

    def get_segment_id(self) -> Optional[int]:
        return self.segment_counter.most_common(1)[0][0]


detailed_trivia_processor = TriviaProcessor()
detailed_trivia_processor.register_tidbit(TotalNumberOfSegmentsTidbit())
detailed_trivia_processor.register_tidbit(TotalUniqueSegmentsTidbit())
detailed_trivia_processor.register_tidbit(MostRanSegmentTidbit())
