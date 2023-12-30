import pytest
from stravalib.model import Activity, PolylineMap
from tests.factories.activity_factories import ActivityFactory
from tests.factories.athlete_factories import AthleteFactory
from tests.factories.best_effort_factories import BestEffortFactory
from tests.factories.segment_factories import SegmentEffortFactory


@pytest.fixture
def some_basic_runs_and_rides() -> list[Activity]:
    athlete = AthleteFactory()
    return [
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Run", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
        ActivityFactory(athlete=athlete, type="Ride", flagged=False),
    ]


@pytest.fixture
def some_basic_runs_and_rides_without_heartrate() -> list[Activity]:
    athlete = AthleteFactory()
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
def no_activities_at_all() -> list[Activity]:
    """
    A list containing zero activities.
    What if a Strava athlete who has never used Strava before in their life wants to use my website?
    Wouldn't that be wild?
    """
    return []


@pytest.fixture
def some_runs_with_best_efforts() -> list[Activity]:
    athlete = AthleteFactory()

    return [
        ActivityFactory(
            athlete=athlete,
            type="Run",
            best_efforts=[BestEffortFactory() for _ in range(5)],
            flagged=False,
        )
        for _ in range(5)
    ]


@pytest.fixture
def some_runs_with_segment_efforts() -> list[Activity]:
    """
    A fixture where each activity gets 5 segment efforts.
    """
    athlete = AthleteFactory()

    return [
        ActivityFactory(
            athlete=athlete,
            type="Run",
            segment_efforts=[SegmentEffortFactory() for _ in range(5)],
        )
        for _ in range(5)
    ]


@pytest.fixture
def activities_with_polylines() -> list[Activity]:
    """
    A list of activities with polylines.
    """
    return [
        ActivityFactory(
            type="Run",
            map=PolylineMap(
                id="123",
                polyline=None,
                summary_polyline="tdufD}|}d\C?e@Nm@\eAn@u@j@_Aj@i@b@q@\EN]HcAZyBdAWVcAt@g@Vs@n@{@j@c@r@mAnAW`@Mb@MVJR@Tw@jAGp@LtALl@RVTf@Vr@b@bBP`@FX?JCp@Jt@Vh@P^PTf@`@l@pABJ`@fA\t@~@hAd@`ARl@z@dBV^rA~AV\hBjDh@lA~BlC`@j@rCxERXdBbBbArAVf@jAjAXRb@LXPzA|ARJVD^TdAz@v@x@Rb@^l@x@`Az@t@dAl@vBvAjBtA`@^hBvAvA`Ap@j@dB`AlDlC~@n@hAh@hA\^Rd@\jAp@RFf@Df@Cf@BbB~@fAp@f@`@`@b@^Tf@Fr@Ah@OX[|@sBvAsDLc@d@eAHe@Hq@N_@FIFUAc@D{@DiEF}B?gBBsAD~CAfCErAEdEG~AJj@@h@GjAc@tD_@zAQf@Sd@{@rAIFa@RWDe@Ga@AWQM[[YWIkAk@s@g@{@g@k@[[Mi@[]IkAFSCWGiAi@{@c@eAs@cAa@mCgB}B}AeCoB{@g@mAcA_Am@uAkAeBgAiBoAc@_@a@c@e@_@}@_Aw@{A[a@u@o@a@WaA_@]Yy@}@w@_@]I_@Wk@i@eDeEWg@aBoB{@mAe@{@aBwBWg@y@gAqA{BqAgB{AeCi@u@sAmC[w@gAkBi@_BUe@w@mA{@iBKgA_@yAMq@Qi@q@_BKsAGc@Ak@Fe@JW`@m@Ie@Ng@PQZe@`@a@p@_AVi@bByAVYhCwAnAaAZO\Kb@Wd@O",
            ),
        )
    ]
