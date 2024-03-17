import boto3
import moto
from active_statistics.gui.tabs import cumulative_time_tab
from active_statistics.utils.environment_variables import EnvironmentVariableManager


# Test that when data for trivia tabs is processed, when S3 is used, that the data is dumped to a json correctly.
@moto.mock_aws
def test_plot_tab(some_basic_runs_and_rides):
    # Create the bucket since this is happening in the moto 'virtual' aws account.
    s3 = boto3.client("s3", region_name="ap-southeast-2")
    s3.create_bucket(
        Bucket="athlete-data-storage",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
    )

    evm = EnvironmentVariableManager(data_storage="s3")
    cumulative_time_tab.backend_processing_hook(some_basic_runs_and_rides, evm, 1)

    # Get the data out of our mock s3 to check that it was inserted.
    body = (
        s3.get_object(
            Bucket="athlete-data-storage", Key="1/cumulative_time/chart.json"
        )["Body"]
        .read()
        .decode("utf-8")
    )

    # # For now just assert that it exists. Nothing fancy.
    assert body
