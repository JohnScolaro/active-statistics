from active_statistics.statistics.trivia.detailed_trivia import (
    detailed_trivia_processor,
)


def test_summary_trivia(some_runs_with_segment_efforts) -> None:
    """
    A basic test to make sure that if we pump some random data through the
    processor, nothing breaks.
    """
    detailed_trivia_processor.get_data(some_runs_with_segment_efforts)
