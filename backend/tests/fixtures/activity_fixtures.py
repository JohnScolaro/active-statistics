import json

import pytest
from stravalib.model import PolylineMap, SummaryActivity

from tests.factories.activity_factories import ActivityFactory
from tests.factories.athlete_factories import MetaAthleteFactory
from tests.fixtures import REAL_DATA


@pytest.fixture
def some_basic_runs_and_rides() -> list[SummaryActivity]:
    athlete = MetaAthleteFactory()
    return [
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
    ]


@pytest.fixture
def some_basic_runs_and_rides_without_heartrate() -> list[SummaryActivity]:
    athlete = MetaAthleteFactory()
    return [
        ActivityFactory(
            athlete=athlete, type="Run", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Run", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Run", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Ride", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Ride", average_heartrate=None, flagged=False
        ),
        ActivityFactory(
            athlete=athlete, type="Ride", average_heartrate=None, flagged=False
        ),
    ]


@pytest.fixture
def no_activities_at_all() -> list[SummaryActivity]:
    """
    A list containing zero activities.
    What if a Strava athlete who has never used Strava before in their life wants to use
    my website? Wouldn't that be wild?
    """
    return []


@pytest.fixture
def activities_with_polylines() -> list[SummaryActivity]:
    """
    A list of activities with polylines.
    """
    return [
        ActivityFactory(
            type="Run",
            map=PolylineMap(
                id="123",
                polyline=None,
                summary_polyline="tdufD}|}d\\C?e@Nm@\\eAn@u@j@_Aj@i@b@q@\\EN]HcAZyBdAWVcAt@g@Vs@n@{@j@c@r@mAnAW`@Mb@MVJR@Tw@jAGp@LtALl@RVTf@Vr@b@bBP`@FX?JCp@Jt@Vh@P^PTf@`@l@pABJ`@fA\t@~@hAd@`ARl@z@dBV^rA~AV\\hBjDh@lA~BlC`@j@rCxERXdBbBbArAVf@jAjAXRb@LXPzA|ARJVD^TdAz@v@x@Rb@^l@x@`Az@t@dAl@vBvAjBtA`@^hBvAvA`Ap@j@dB`AlDlC~@n@hAh@hA\\^Rd@\\jAp@RFf@Df@Cf@BbB~@fAp@f@`@`@b@^Tf@Fr@Ah@OX[|@sBvAsDLc@d@eAHe@Hq@N_@FIFUAc@D{@DiEF}B?gBBsAD~CAfCErAEdEG~AJj@@h@GjAc@tD_@zAQf@Sd@{@rAIFa@RWDe@Ga@AWQM[[YWIkAk@s@g@{@g@k@[[Mi@[]IkAFSCWGiAi@{@c@eAs@cAa@mCgB}B}AeCoB{@g@mAcA_Am@uAkAeBgAiBoAc@_@a@c@e@_@}@_Aw@{A[a@u@o@a@WaA_@]Yy@}@w@_@]I_@Wk@i@eDeEWg@aBoB{@mAe@{@aBwBWg@y@gAqA{BqAgB{AeCi@u@sAmC[w@gAkBi@_BUe@w@mA{@iBKgA_@yAMq@Qi@q@_BKsAGc@Ak@Fe@JW`@m@Ie@Ng@PQZe@`@a@p@_AVi@bByAVYhCwAnAaAZO\\Kb@Wd@O",
            ),
        )
    ]


@pytest.fixture
def real_activities() -> list[SummaryActivity]:
    """
    A bunch of real activities using my own data to test.
    """
    with open(REAL_DATA, "r") as f:
        data = json.load(f)

    return [SummaryActivity.model_validate(obj) for obj in data]

    # json_string = json.load("94896104.json")
    # return json_string
