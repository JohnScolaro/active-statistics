from active_statistics.statistics.trivia.summary_trivia import general_trivia


def test_summary_trivia(some_basic_runs_and_rides) -> None:
    """
    A basic test to make sure that if we pump some random data through the
    processor, nothing breaks.
    """
    general_trivia.get_data(some_basic_runs_and_rides)


def test_summary_trivia_no_activities() -> None:
    """
    A basic test to make sure that if we pump some random data through the
    processor, nothing breaks.
    """
    general_trivia.get_data(_ for _ in [])
