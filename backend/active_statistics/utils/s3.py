"""
A collection of helpers for all s3 related tasks.
"""

from typing import Optional

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "athlete-data-storage"

# Create an S3 client
s3 = boto3.client("s3")


def get_visualisation_data(athlete_id: int, tab_key: str) -> Optional[str]:
    try:
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=get_s3_key_from_athlete_and_tab_key(athlete_id, tab_key),
        )
        chart_json = response["Body"].read()
        return chart_json.decode("utf-8")

    except ClientError as e:
        # Honestly we don't really care what the error is, if there is an error, just return None.
        # In the future we could check if e.response["Error"]["Code"] == "NoSuchKey" or something,
        # but for now, this is fine.
        return None


def save_plot_data(athlete_id: int, tab_key: str, chart_json: str) -> None:
    # Upload the chart json to the S3 bucket
    s3.put_object(
        Body=chart_json,
        Bucket=BUCKET_NAME,
        Key=get_s3_key_from_athlete_and_tab_key(athlete_id, tab_key),
    )


def is_there_any_data_for_athlete(athlete_id: int) -> bool:
    s3 = boto3.client("s3")

    # Check if there are any objects in the folder
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=str(athlete_id) + "/")
    return bool(len(response["Contents"]))


def get_s3_key_from_athlete_and_tab_key(athlete_id: int, tab_key: str) -> str:
    return f"{str(athlete_id)}/{tab_key}.json"
