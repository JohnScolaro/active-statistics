import pytest
from stravalib.model import Athlete

from tests.factories.athlete_factories import AthleteFactory


@pytest.fixture
def mock_generic_athlete() -> Athlete:
    """
    Just a boring test athlete with dummy data.
    """
    return AthleteFactory()
