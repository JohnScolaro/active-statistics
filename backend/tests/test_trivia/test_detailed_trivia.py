from active_statistics.statistics.trivia.detailed_trivia import (
    detailed_trivia_processor,
)


def test_detailed_trivia(some_runs_with_segment_efforts) -> None:
    """
    A basic test to make sure that if we pump some random data through the
    processor, nothing breaks.
    """
    detailed_trivia_processor.get_data(some_runs_with_segment_efforts)


def test_detailed_trivia_with_no_segments(some_basic_runs_and_rides) -> None:
    """
    When analysing segments, if the user has no activities with segments, this
    tidbit should return None instead of breaking.
    """
    detailed_trivia_processor.get_data(some_basic_runs_and_rides)
