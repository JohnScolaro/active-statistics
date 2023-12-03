from collections import Counter
from typing import Optional

from active_statistics.statistics.trivia import TriviaProcessor, TriviaTidbitBase
from stravalib.model import Activity


class TotalNumberOfSegmentsTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.segment_count = 0

    def process_activity(self, activity: Activity) -> None:
        if activity.segment_efforts is not None:
            self.segment_count += len(activity.segment_efforts)

    def get_description(self) -> str:
        return "Total Number of Segments Completed"

    def get_tidbit(self) -> Optional[str]:
        return str(self.segment_count)

    def reset_tidbit(self) -> None:
        self.segment_count = 0


class TotalUniqueSegmentsTidbit(TriviaTidbitBase):
    def __init__(self) -> None:
        self.segment_counter: Counter[int] = Counter()

    def reset_tidbit(self) -> None:
        self.segment_counter = Counter()

    def process_activity(self, activity: Activity) -> None:
        if activity.segment_efforts is not None:
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

    def reset_tidbit(self) -> None:
        self.segment_counter = Counter()

    def process_activity(self, activity: Activity) -> None:
        if activity.segment_efforts is not None:
            self.segment_counter.update(
                segment_effort.segment.id for segment_effort in activity.segment_efforts
            )

    def get_description(self) -> str:
        return "Most Popular Segment"

    def get_tidbit(self) -> Optional[str]:
        most_common_segment = self.segment_counter.most_common(1)
        if not most_common_segment:
            return None

        segment_id, num_completions = most_common_segment[0]
        return f"{num_completions} completions"

    def get_segment_id(self) -> Optional[int]:
        return self.segment_counter.most_common(1)[0][0]


detailed_trivia_processor = TriviaProcessor()
detailed_trivia_processor.register_tidbit(TotalNumberOfSegmentsTidbit())
detailed_trivia_processor.register_tidbit(TotalUniqueSegmentsTidbit())
detailed_trivia_processor.register_tidbit(MostRanSegmentTidbit())
