import shutil

import pytest
from active_statistics.statistics.images.polyline_overlay import create_images
from stravalib.model import Activity, PolylineMap
from tests.factories.activity_factories import ActivityFactory


@pytest.fixture(scope="function")
def temp_directory(request, tmp_path_factory):
    # Create a temporary directory
    temp_dir = tmp_path_factory.mktemp("temp_directory")

    # Define a finalizer to clean up the directory after the test
    def cleanup_temp_directory():
        # Delete the directory and its contents
        shutil.rmtree(temp_dir)

    # Add the finalizer to the request to ensure cleanup
    request.addfinalizer(cleanup_temp_directory)

    return temp_dir


class TestPolylineOverlay:
    def test_no_activities(self, temp_directory) -> None:
        activities: list[Activity] = []
        create_images((_ for _ in activities), temp_directory)

    def test_activities_with_no_polylines(self, temp_directory) -> None:
        activities = [
            ActivityFactory(
                type="Run",
                map=PolylineMap(id="123", polyline=None, summary_polyline=None),
            ),
        ]
        create_images((_ for _ in activities), temp_directory)

    def test_activities_with_blank_polylines(self, temp_directory) -> None:
        activities: list[Activity] = [
            ActivityFactory(
                type="Run",
                map=PolylineMap(id="123", polyline=None, summary_polyline=""),
            ),
        ]
        create_images((_ for _ in activities), temp_directory)

    def test_activities_with_single_point_polylines(self, temp_directory) -> None:
        activities: list[Activity] = [
            ActivityFactory(
                type="Run",
                map=PolylineMap(id="123", polyline=None, summary_polyline="??"),
            ),
        ]
        create_images((_ for _ in activities), temp_directory)

    def test_activities_with_multi_point_identical_polylines(
        self, temp_directory
    ) -> None:
        # Yes, this polyline is from real data.
        activities: list[Activity] = [
            ActivityFactory(
                type="Run",
                map=PolylineMap(
                    id="123", polyline=None, summary_polyline="fszfDwsbe\\??"
                ),
            ),
        ]
        create_images((_ for _ in activities), temp_directory)

    def test_activities_with_normal_polylines(self, temp_directory) -> None:
        activities: list[Activity] = [
            ActivityFactory(
                type="Run",
                map=PolylineMap(
                    id="123",
                    polyline=None,
                    summary_polyline="tdufD}|}d\C?e@Nm@\eAn@u@j@_Aj@i@b@q@\EN]HcAZyBdAWVcAt@g@Vs@n@{@j@c@r@mAnAW`@Mb@MVJR@Tw@jAGp@LtALl@RVTf@Vr@b@bBP`@FX?JCp@Jt@Vh@P^PTf@`@l@pABJ`@fA\t@~@hAd@`ARl@z@dBV^rA~AV\hBjDh@lA~BlC`@j@rCxERXdBbBbArAVf@jAjAXRb@LXPzA|ARJVD^TdAz@v@x@Rb@^l@x@`Az@t@dAl@vBvAjBtA`@^hBvAvA`Ap@j@dB`AlDlC~@n@hAh@hA\^Rd@\jAp@RFf@Df@Cf@BbB~@fAp@f@`@`@b@^Tf@Fr@Ah@OX[|@sBvAsDLc@d@eAHe@Hq@N_@FIFUAc@D{@DiEF}B?gBBsAD~CAfCErAEdEG~AJj@@h@GjAc@tD_@zAQf@Sd@{@rAIFa@RWDe@Ga@AWQM[[YWIkAk@s@g@{@g@k@[[Mi@[]IkAFSCWGiAi@{@c@eAs@cAa@mCgB}B}AeCoB{@g@mAcA_Am@uAkAeBgAiBoAc@_@a@c@e@_@}@_Aw@{A[a@u@o@a@WaA_@]Yy@}@w@_@]I_@Wk@i@eDeEWg@aBoB{@mAe@{@aBwBWg@y@gAqA{BqAgB{AeCi@u@sAmC[w@gAkBi@_BUe@w@mA{@iBKgA_@yAMq@Qi@q@_BKsAGc@Ak@Fe@JW`@m@Ie@Ng@PQZe@`@a@p@_AVi@bByAVYhCwAnAaAZO\Kb@Wd@O",
                ),
            ),
        ]
        create_images((_ for _ in activities), temp_directory)
