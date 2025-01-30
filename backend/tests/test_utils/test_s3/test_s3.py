import boto3
from moto import mock_aws

from backend.utils.s3 import (
    BUCKET_NAME,
    get_summary_activities_from_s3,
    save_summary_activities_to_s3,
)


@mock_aws
def test_saving_activity_roundtrip(some_basic_runs_and_rides) -> None:
    s3_client = boto3.client("s3", region_name="ap-southeast-2")
    s3_client.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
    )

    save_summary_activities_to_s3(s3_client, 123, some_basic_runs_and_rides)
    reloaded_activities = get_summary_activities_from_s3(s3_client, 123)

    for fixture_activity, reloaded_activity in zip(
        some_basic_runs_and_rides, reloaded_activities
    ):
        assert fixture_activity == reloaded_activity
