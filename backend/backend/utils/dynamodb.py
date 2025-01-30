import datetime as dt

from botocore.exceptions import ClientError
from fastapi import HTTPException
from mypy_boto3_dynamodb.service_resource import Table
from pydantic import BaseModel
from stravalib.protocol import AccessInfo

TTL_TIME_IN_FUTURE = 7 * 24 * 60 * 60  # Number of seconds in a week


class UserTableItem(BaseModel):
    session_token: str
    athlete_id: int
    access_token: str
    refresh_token: str
    expires_at: int


class DownloadStatusItem(BaseModel):
    athlete_id: int
    last_download_time: dt.datetime
    status: str
    ttl: dt.datetime
    error: bool


def save_user_data_to_dynamo(
    user_table: Table, session_token: str, athlete_id: int, access_info: AccessInfo
) -> None:
    try:
        # Use the attributes from the Pydantic model
        user_table.update_item(
            Key={"session_token": session_token},
            UpdateExpression=(
                "SET access_token = :access_token, "
                "refresh_token = :refresh_token, "
                "expires_at = :expires_at, "
                "athlete_id = :athlete_id"
            ),
            ExpressionAttributeValues={
                ":access_token": access_info["access_token"],
                ":refresh_token": access_info["refresh_token"],
                ":expires_at": access_info["expires_at"],
                ":athlete_id": athlete_id,
            },
            ReturnValues="ALL_NEW",
        )
        print(f"Successfully upserted user {athlete_id}.")
    except ClientError as e:
        print(f"Error upserting user: {e.response['Error']['Message']}")
        raise e


def get_athlete_id_from_session_token(user_table: Table, session_token: str) -> int:
    try:
        response = user_table.get_item(Key={"session_token": session_token})
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB error: {str(e)}")

    if "Item" not in response:
        raise Exception(f"Can't find athlete with session token: {session_token}")
    return int(response["Item"]["athlete_id"])


def get_user_data_row_for_athlete(
    user_table: Table, session_token: str
) -> UserTableItem:
    try:
        response = user_table.get_item(Key={"session_token": session_token})
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB error: {str(e)}")

    if "Item" not in response:
        raise Exception(f"Can't find athlete with session token: {session_token}")
    return UserTableItem(
        session_token=response["Item"]["session_token"],
        athlete_id=response["Item"]["athlete_id"],
        access_token=response["Item"]["access_token"],
        refresh_token=response["Item"]["refresh_token"],
        expires_at=response["Item"]["expires_at"],
    )


def save_download_status_to_dynamo(
    download_status_table: Table,
    athlete_id: int,
    download_time: dt.datetime,
    status: str,
    error: bool,
) -> None:
    try:
        # Use the attributes from the Pydantic model
        response = download_status_table.update_item(
            Key={"athlete_id": athlete_id},
            UpdateExpression=(
                "SET last_download_time = :last_download_time, "
                "status_message = :status_message, "
                "time_to_live = :time_to_live, "
                "download_error = :download_error"
            ),
            ExpressionAttributeValues={
                ":last_download_time": int(download_time.timestamp()),
                ":status_message": status,
                ":time_to_live": int(download_time.timestamp()) + TTL_TIME_IN_FUTURE,
                ":download_error": error,
            },
            ReturnValues="ALL_NEW",
        )
        print(f"Successfully upserted athlete: {athlete_id}.")
    except ClientError as e:
        print(f"Error upserting athlete: {e.response['Error']['Message']}")
        raise e


def get_download_status_item_from_dynamo(
    download_status_table: Table, athlete_id: int
) -> DownloadStatusItem | None:
    """
    Returns a DownloadStatusItem for a user from dynamodb, and just returns None if
    there isn't an item for that athlete.
    """
    try:
        response = download_status_table.get_item(Key={"athlete_id": athlete_id})
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB error: {str(e)}")

    if "Item" not in response:
        return None
    else:
        return DownloadStatusItem(
            athlete_id=response["Item"]["athlete_id"],
            last_download_time=dt.datetime.fromtimestamp(
                int(response["Item"]["last_download_time"]), tz=dt.timezone.utc
            ),
            status=response["Item"]["status_message"],
            ttl=response["Item"]["time_to_live"],
            error=response["Item"]["download_error"],
        )
