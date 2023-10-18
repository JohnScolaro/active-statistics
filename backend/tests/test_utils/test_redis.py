import datetime as dt

import freezegun
import pytest
from active_statistics.utils import redis
from pytest import MonkeyPatch
from stravalib.protocol import AccessInfo


class TestRedisSummaryRefreshTime:
    @pytest.fixture
    def monkeypatch_redis_client(self, monkeypatch: MonkeyPatch, redisdb) -> None:
        monkeypatch.setattr(redis, "r_last_summary_refresh", redisdb)

    @freezegun.freeze_time("2000-1-1 00:00:00")
    def test_set_and_get_time(self, monkeypatch_redis_client):
        redis.set_last_summary_refresh_time(1)
        assert redis.get_last_summary_refresh_time(1) == dt.datetime(2000, 1, 1)

    def test_get_no_time(self, monkeypatch_redis_client):
        """Test that getting the time when it's never been recorded returns Null."""
        assert redis.get_last_summary_refresh_time(1) is None


class TestRedisDetailedRefreshTime:
    @pytest.fixture
    def monkeypatch_redis_client(self, monkeypatch: MonkeyPatch, redisdb) -> None:
        monkeypatch.setattr(redis, "r_last_detailed_refresh", redisdb)

    @freezegun.freeze_time("2000-1-1 00:00:00")
    def test_set_and_get_time(self, monkeypatch_redis_client):
        redis.set_last_detailed_refresh_time(1)
        assert redis.get_last_detailed_refresh_time(1) == dt.datetime(2000, 1, 1)

    def test_get_no_time(self, monkeypatch_redis_client):
        """Test that getting the time when it's never been recorded returns Null."""
        assert redis.get_last_detailed_refresh_time(1) is None


class TestRedisAccessKeys:
    @pytest.fixture
    def monkeypatch_redis_client(self, monkeypatch: MonkeyPatch, redisdb) -> None:
        monkeypatch.setattr(redis, "r_api_access", redisdb)

    def test_set_strava_access_tokens(self, monkeypatch_redis_client):
        """Test that getting the time when it's never been recorded returns Null."""
        redis.set_strava_access_tokens(
            1,
            AccessInfo(
                access_token="test1",
                refresh_token="test2",
                expires_at=int(dt.datetime(2000, 1, 1).timestamp()),
            ),
        )

        assert redis.get_strava_api_access_token(1) == "test1"
        assert redis.get_strava_api_refresh_token(1) == "test2"
        assert redis.get_strava_api_access_token_expires_at(1) == dt.datetime(
            2000, 1, 1
        )

    def test_get_strava_access_tokens_when_dont_exist(self, monkeypatch_redis_client):
        assert redis.get_strava_api_access_token(1) == None
        assert redis.get_strava_api_refresh_token(1) == None
        assert redis.get_strava_api_access_token_expires_at(1) == None
