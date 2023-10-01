from typing import Generator

import pytest
from active_statistics.utils import rq
from pytest import MonkeyPatch


@pytest.fixture
def monkeypatch_redis_client(monkeypatch: MonkeyPatch, redisdb) -> None:
    monkeypatch.setattr(rq, "r_task_queue", redisdb)


@pytest.fixture
def reset_queues_after_test() -> Generator[None, None, None]:
    yield
    rq.summary_queue.empty()
    rq.detailed_queue.empty()


class TestRQDetailedTask:
    def test_enqueue_and_get_position(
        self, monkeypatch_redis_client, reset_queues_after_test
    ) -> None:
        """
        Enqueue an rq task and make sure that we can tell that it's queued.
        """
        rq.enqueue_detailed_task(1)
        assert rq.get_position_in_detailed_queue(1) == 1

    def test_multiple_queue_members(
        self, monkeypatch_redis_client, reset_queues_after_test
    ) -> None:
        """
        Enqueue multiple jobs and check we can get their position in the queue.
        """
        rq.enqueue_detailed_task(1)
        rq.enqueue_detailed_task(2)
        rq.enqueue_detailed_task(3)
        assert rq.get_position_in_detailed_queue(1) == 1
        assert rq.get_position_in_detailed_queue(2) == 2
        assert rq.get_position_in_detailed_queue(3) == 3

    def test_unknown_job_status(
        self, monkeypatch_redis_client, reset_queues_after_test
    ) -> None:
        assert rq.get_detailed_task_job_status(1) == None

    def test_unknown_job_position_in_queue(
        self, monkeypatch_redis_client, reset_queues_after_test
    ) -> None:
        assert rq.get_position_in_detailed_queue(1) == None


class TestRQSummaryTask:
    def test_enqueue_and_get_position(
        self, monkeypatch_redis_client, reset_queues_after_test
    ) -> None:
        """
        Enqueue an rq task and make sure that we can tell that it's queued.
        """
        rq.enqueue_summary_task(1)
        assert rq.get_position_in_summary_queue(1) == 1

    def test_multiple_queue_members(
        self, monkeypatch_redis_client, reset_queues_after_test
    ) -> None:
        """
        Enqueue multiple jobs and check we can get their position in the queue.
        """
        rq.enqueue_summary_task(1)
        rq.enqueue_summary_task(2)
        rq.enqueue_summary_task(3)
        assert rq.get_position_in_summary_queue(1) == 1
        assert rq.get_position_in_summary_queue(2) == 2
        assert rq.get_position_in_summary_queue(3) == 3

    def test_unknown_job_status(
        self, monkeypatch_redis_client, reset_queues_after_test
    ) -> None:
        assert rq.get_summary_task_job_status(1) == None

    def test_unknown_job_position_in_queue(
        self, monkeypatch_redis_client, reset_queues_after_test
    ) -> None:
        assert rq.get_position_in_summary_queue(1) == None
