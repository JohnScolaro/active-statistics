import datetime as dt

import boto3
import pytest
from moto import mock_aws

from backend.utils.dynamodb import (
    get_athlete_id_from_session_token,
    get_download_status_item_from_dynamo,
    get_user_data_row_for_athlete,
    save_download_status_to_dynamo,
)

USER_TABLE_NAME = "user-table"
DOWNLOAD_STATUS_NAME = "download-status-table"


@mock_aws
def test_get_athlete_id_from_session_token_when_athlete_doesnt_exist():
    name = USER_TABLE_NAME
    conn = boto3.client(
        "dynamodb",
        region_name="ap-southeast-2",
        aws_access_key_id="ak",
        aws_secret_access_key="sk",
    )
    conn.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "session_token", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "session_token", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    dynamodb = boto3.resource("dynamodb")
    user_table = dynamodb.Table(USER_TABLE_NAME)
    with pytest.raises(Exception, match="Can't find athlete"):
        get_athlete_id_from_session_token(user_table, "no_athlete_session_token")


@mock_aws
def test_get_athlete_id_from_session_token_when_athlete_does_exist():
    name = USER_TABLE_NAME
    client = boto3.client(
        "dynamodb",
        region_name="ap-southeast-2",
        aws_access_key_id="ak",
        aws_secret_access_key="sk",
    )
    client.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "session_token", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "session_token", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    client.put_item(
        TableName=USER_TABLE_NAME,
        Item={
            "session_token": {"S": "example_session_token"},
            "athlete_id": {"N": "1"},
            "access_token": {"S": "a"},
            "refresh_token": {"S": "b"},
            "expires_at": {"N": "2"},
        },
    )
    user_table = boto3.resource("dynamodb").Table(USER_TABLE_NAME)
    assert get_athlete_id_from_session_token(user_table, "example_session_token") == 1


@mock_aws
def test_save_data_status_to_dynamodb() -> None:
    conn = boto3.client(
        "dynamodb",
        region_name="ap-southeast-2",
        aws_access_key_id="ak",
        aws_secret_access_key="sk",
    )
    conn.create_table(
        TableName=DOWNLOAD_STATUS_NAME,
        KeySchema=[{"AttributeName": "athlete_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "athlete_id", "AttributeType": "N"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    data_status_table = boto3.resource("dynamodb").Table(DOWNLOAD_STATUS_NAME)
    save_download_status_to_dynamo(
        data_status_table,
        1,
        dt.datetime(2020, 1, 2, tzinfo=dt.timezone.utc),
        "yeet",
        error=False,
    )
    request = data_status_table.get_item(Key={"athlete_id": 1})
    assert "Item" in request
    assert int(request["Item"]["athlete_id"]) == 1


@mock_aws
def test_get_last_downloaded_status_item_from_dynamo_when_it_doesnt_exist() -> None:
    name = DOWNLOAD_STATUS_NAME
    conn = boto3.client(
        "dynamodb",
        region_name="ap-southeast-2",
        aws_access_key_id="ak",
        aws_secret_access_key="sk",
    )
    conn.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "athlete_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "athlete_id", "AttributeType": "N"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    download_status_table = boto3.resource("dynamodb").Table(DOWNLOAD_STATUS_NAME)
    assert get_download_status_item_from_dynamo(download_status_table, 1) is None


@mock_aws
def test_get_last_downloaded_status_item_from_dynamo() -> None:
    name = DOWNLOAD_STATUS_NAME
    conn = boto3.client(
        "dynamodb",
        region_name="ap-southeast-2",
        aws_access_key_id="ak",
        aws_secret_access_key="sk",
    )
    conn.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "athlete_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "athlete_id", "AttributeType": "N"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    data_status_table = boto3.resource("dynamodb").Table(DOWNLOAD_STATUS_NAME)
    save_download_status_to_dynamo(
        data_status_table,
        1,
        dt.datetime(2024, 1, 1, 1, 1, 1, tzinfo=dt.timezone.utc),
        "yeet",
        error=False,
    )
    download_status_row = get_download_status_item_from_dynamo(data_status_table, 1)
    assert download_status_row.athlete_id == 1
    assert download_status_row.last_download_time == dt.datetime(
        2024, 1, 1, 1, 1, 1, tzinfo=dt.timezone.utc
    )
    assert download_status_row.status == "yeet"
    assert download_status_row.ttl == dt.datetime(
        2024, 1, 1, 1, 1, 1, tzinfo=dt.timezone.utc
    ) + dt.timedelta(days=7)
    assert download_status_row.error == False


@mock_aws
def test_get_user_data_row_for_athlete():
    name = USER_TABLE_NAME
    conn = boto3.client(
        "dynamodb",
        region_name="ap-southeast-2",
        aws_access_key_id="ak",
        aws_secret_access_key="sk",
    )
    conn.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "session_token", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "session_token", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    conn.put_item(
        TableName=USER_TABLE_NAME,
        Item={
            "session_token": {"S": "example_session_token"},
            "athlete_id": {"N": "1"},
            "access_token": {"S": "a"},
            "refresh_token": {"S": "b"},
            "expires_at": {"N": "2"},
        },
    )

    user_table = boto3.resource("dynamodb").Table(USER_TABLE_NAME)
    row = get_user_data_row_for_athlete(user_table, "example_session_token")
    assert row.session_token == "example_session_token"
    assert row.athlete_id == 1
    assert row.access_token == "a"
    assert row.refresh_token == "b"
    assert row.expires_at == 2
