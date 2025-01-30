import pytest
from stravalib.model import SummaryAthlete

from tests.factories.athlete_factories import AthleteFactory


@pytest.fixture
def mock_generic_athlete() -> SummaryAthlete:
    """
    Just a boring test athlete with dummy data.
    """
    return AthleteFactory()
