"""
A collection of helpers for all s3 related tasks.
"""

from typing import Optional

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "athlete-data-storage"

# Create an S3 client
s3 = boto3.client("s3")


def get_tab_data(athlete_id: int, tab_key: str) -> Optional[str]:
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


def save_tab_data(athlete_id: int, tab_key: str, chart_json: str) -> None:
    # Upload the chart json to the S3 bucket
    s3.put_object(
        Body=chart_json,
        Bucket=BUCKET_NAME,
        Key=get_s3_key_from_athlete_and_tab_key(athlete_id, tab_key),
    )


def save_tab_images(athlete_id: int, tab_key: str, paths: list[str]) -> None:
    for path in paths:
        s3.upload_file(
            Filename=f"{tab_key}/{path}/",
            Bucket=BUCKET_NAME,
            Key=get_s3_key_from_athlete_and_tab_key(athlete_id, tab_key),
        )


def get_tab_images(athlete_id: int, tab_key: str) -> list[str]:
    # List all objects in the S3 directory
    try:
        objects = s3.list_objects_v2(
            Bucket=BUCKET_NAME, Prefix=f"{athlete_id}/{tab_key}/"
        )
    except:
        raise Exception("Something went wrong while trying to list images.")

    presigned_urls: list[str] = []
    # Generate pre-signed URLs for each image
    for obj in objects.get("Contents", []):
        object_key = obj["Key"]
        # Generate a pre-signed URL with a 1-hour expiration
        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": object_key},
            ExpiresIn=3600,  # URL expiration time in seconds (1 hour)
        )
        presigned_urls.append(presigned_url)

    return presigned_urls


def is_there_any_data_for_athlete(athlete_id: int) -> bool:
    s3 = boto3.client("s3")

    # Check if there are any objects in the folder
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=str(athlete_id) + "/")
    return bool(len(response["Contents"]))


def get_s3_key_from_athlete_and_tab_key(athlete_id: int, tab_key: str) -> str:
    return f"{str(athlete_id)}/{tab_key}.json"
