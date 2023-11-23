"""
A collection of helpers for all s3 related tasks.
"""

import json
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "athlete-data-storage"

# Create an S3 client
s3 = boto3.client("s3")


def get_object(athlete_id: int, tab_key: str, filename: str) -> str:
    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=f"{athlete_id}/{tab_key}/{filename}",
    )
    chart_json = response["Body"].read()
    return chart_json.decode("utf-8")


def upload_file(athlete_id: int, tab_key: str, filename: str) -> None:
    # Upload the chart json to the S3 bucket
    s3.upload_file(
        Filename=filename,
        Bucket=BUCKET_NAME,
        Key=get_s3_key(athlete_id, tab_key, os.path.basename(filename)),
    )


def save_chart_json(athlete_id: int, tab_key: str, chart_json: str) -> None:
    # Upload the chart json to the S3 bucket
    s3.put_object(
        Body=chart_json,
        Bucket=BUCKET_NAME,
        Key=get_s3_key(athlete_id, tab_key, "chart.json"),
    )


def save_table_json(athlete_id: int, tab_key: str, table_json: str) -> None:
    # Upload the table json to the S3 bucket
    s3.put_object(
        Body=table_json,
        Bucket=BUCKET_NAME,
        Key=get_s3_key(athlete_id, tab_key, "table.json"),
    )


def get_pre_signed_urls_for_tab_images(athlete_id: int, tab_key: str) -> dict[str, str]:
    # List all objects in the S3 directory
    try:
        objects = s3.list_objects_v2(
            Bucket=BUCKET_NAME, Prefix=f"{athlete_id}/{tab_key}/"
        )
    except:
        raise Exception("Something went wrong while trying to list images.")

    presigned_urls: dict[str, str] = {}
    # Generate pre-signed URLs for each image
    for obj in objects.get("Contents", []):
        object_key = obj["Key"]

        # Exclude .json objects because our captions are stored as json blobs in this directory.
        if object_key.endswith(".json"):
            continue

        # Generate a pre-signed URL with a 1-hour expiration
        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": object_key},
            ExpiresIn=3600,  # URL expiration time in seconds (1 hour)
        )

        # Just split the s3 URL manually to get the file name
        presigned_urls[object_key.split("/")[-1]] = presigned_url

    return presigned_urls


def get_captions_for_tab_images(athlete_id: int, tab_key: str) -> dict[str, str]:
    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=f"{athlete_id}/{tab_key}/captions.json",
    )
    chart_json = response["Body"].read()
    captions: dict[str, str] = json.loads(chart_json.decode("utf-8"))
    return captions


def is_there_any_data_for_athlete(athlete_id: int) -> bool:
    s3 = boto3.client("s3")

    # Check if there are any objects in the folder
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=str(athlete_id) + "/")
    return bool(len(response["Contents"]))


def get_s3_key(athlete_id: int, tab_key: str, file_name: str) -> str:
    return f"{str(athlete_id)}/{tab_key}/{file_name}"
