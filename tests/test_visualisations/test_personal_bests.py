import pytest

from active_statistics.exceptions import UserVisibleException
from active_statistics.visualisations.personal_bests import plot


def test_personal_bests(some_runs_with_best_efforts) -> None:
    plot(some_runs_with_best_efforts)


def test_no_data(no_activities_at_all) -> None:
    with pytest.raises(UserVisibleException):
        plot(no_activities_at_all)
