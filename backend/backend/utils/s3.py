"""
A collection of helpers for all s3 related tasks.
"""

import datetime as dt
import json

import plotly
from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3Client
from stravalib.model import SummaryActivity

BUCKET_NAME = "athlete-data-storage"


def is_there_any_data_for_athlete(s3_client: S3Client, athlete_id: int) -> bool:
    """
    Returns True if the data for a given athlete exists, and False if it doesnt.
    """
    # Check if there are any objects in the folder
    try:
        s3_client.head_object(Bucket=BUCKET_NAME, Key=str(athlete_id))
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        # Re-raise for any unexpected error
        raise


def get_age_of_data_for_athlete(s3_client: S3Client, athlete_id: int) -> dt.timedelta:
    """
    Returns the age of the blob in the bucket. If it doesn't exist it raises an
    exception.
    """
    try:
        # Fetch the object's metadata
        response = s3_client.head_object(Bucket=BUCKET_NAME, Key=str(athlete_id))
        last_modified = response["LastModified"]
        current_time = dt.datetime.now(dt.timezone.utc)

        # Calculate the age of the data
        age = current_time - last_modified
        return age
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise FileNotFoundError(
                f"Data for athlete_id {athlete_id} does not exist in the bucket."
            )
        # Re-raise for any other unexpected error
        raise


def delete_athlete_data(s3_client: S3Client, athlete_id: int) -> None:
    """
    Given an athlete's ID, delete their data from S3.
    """
    try:
        # Attempt to delete the object corresponding to the athlete_id
        response = s3_client.delete_object(Bucket=BUCKET_NAME, Key=str(athlete_id))
        # You can check the response if needed
        # print(response)  # For debugging purposes
    except ClientError as e:
        # Handle any errors that occur during the delete operation
        print(f"Error deleting data for athlete {athlete_id}: {e}")
        raise


def save_summary_activities_to_s3(
    s3_client: S3Client, athlete_id: int, summary_activities: list[SummaryActivity]
) -> None:
    """
    Saves all the data for an athlete into s3 under their athlete id. If data
    for that athlete already exists, it is deleted and replaced.
    """
    # Serialize the activities to JSON
    activities_data = [activity.model_dump() for activity in summary_activities]
    json_data = json.dumps(activities_data, cls=plotly.utils.PlotlyJSONEncoder)

    # Remove existing data for the athlete if it exists
    if is_there_any_data_for_athlete(s3_client, athlete_id):
        try:
            # Delete the current athlete's data
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=str(athlete_id))
        except ClientError as e:
            raise RuntimeError(
                f"Failed to delete existing data for athlete {athlete_id}"
            ) from e

    # Upload the new data to S3
    try:
        s3_client.put_object(Bucket=BUCKET_NAME, Key=str(athlete_id), Body=json_data)
    except ClientError as e:
        raise RuntimeError(f"Failed to save data for athlete {athlete_id}") from e


def get_summary_activities_from_s3(
    s3_client: S3Client, athlete_id: int
) -> list[SummaryActivity]:
    """
    Given an athletes id, return the list of summary activities that has been stored in
    s3.
    """
    # Get object from S3
    object = s3_client.get_object(Bucket=BUCKET_NAME, Key=str(athlete_id))

    json_data = json.loads(object["Body"].read())

    activities = [SummaryActivity.model_validate(activity) for activity in json_data]

    return activities
