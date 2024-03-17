import boto3
import moto
from active_statistics.gui.tabs import polyline_overlay_tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager


# Test that when data for trivia tabs is processed, when S3 is used, that the data is dumped to a json correctly.
@moto.mock_aws
def test_image_tab(activities_with_polylines):
    # Create the bucket since this is happening in the moto 'virtual' aws account.
    s3 = boto3.client("s3", region_name="ap-southeast-2")
    s3.create_bucket(
        Bucket="athlete-data-storage",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
    )

    evm = EnvironmentVariableManager(data_storage="s3")
    polyline_overlay_tab.backend_processing_hook(activities_with_polylines, evm, 1)

    # Check to see there is data in s3.
    contents = set(
        content["Key"]
        for content in s3.list_objects_v2(Bucket="athlete-data-storage", Prefix="1")[
            "Contents"
        ]
    )
    assert "1/polyline_overlay/Run.png" in contents
    assert "1/polyline_overlay/Run_animation.gif" in contents
    assert "1/polyline_overlay/captions.json" in contents
