from typing import Optional

from active_statistics.constants import DATA_TIMEOUT_SECONDS
from active_statistics.rq_tasks import (
    get_and_process_detailed_statistics,
    get_and_process_summary_statistics,
)
from active_statistics.utils.redis import r_task_queue
from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus

# Default timeout = 10 mins
summary_queue = Queue("summary_queue", connection=r_task_queue, default_timeout=600)

# Default timeout = 2 hours
detailed_queue = Queue(
    "detailed_queue", connection=r_task_queue, default_timeout=3600 * 2
)


def enqueue_detailed_task(athlete_id: int) -> Job:
    job = Job.create(
        get_and_process_detailed_statistics,
        connection=r_task_queue,
        args=(athlete_id,),
        id=get_detailed_job_id(athlete_id),
        result_ttl=DATA_TIMEOUT_SECONDS,
    )
    detailed_queue.enqueue_job(job)
    return job


def enqueue_summary_task(athlete_id: int) -> Job:
    job = Job.create(
        get_and_process_summary_statistics,
        connection=r_task_queue,
        args=(athlete_id,),
        id=get_summary_job_id(athlete_id),
        result_ttl=DATA_TIMEOUT_SECONDS,
    )
    summary_queue.enqueue_job(job)
    return job


def get_detailed_task_job_status(athlete_id: int) -> Optional[JobStatus]:
    """
    Gets the status of a job.
    Returns None when the job is unknown.
    """
    try:
        job = Job.fetch(get_detailed_job_id(athlete_id), connection=r_task_queue)
        return job.get_status()
    except NoSuchJobError:
        return None


def get_summary_task_job_status(athlete_id: int) -> Optional[JobStatus]:
    """
    Gets the status of a job.
    Returns None when the job is unknown.
    """
    try:
        job = Job.fetch(get_summary_job_id(athlete_id), connection=r_task_queue)
        return job.get_status()
    except NoSuchJobError:
        return None


def get_detailed_job_message(athlete_id: int) -> Optional[str]:
    """
    Returns the live job message.
    """
    job = Job.fetch(get_detailed_job_id(athlete_id), connection=r_task_queue)
    job.refresh()
    if "message" in job.meta:
        message: str = job.meta["message"]
        return message
    else:
        return None


def get_summary_job_message(athlete_id: int) -> Optional[str]:
    """
    Returns the live job message.
    """
    job = Job.fetch(get_summary_job_id(athlete_id), connection=r_task_queue)
    job.refresh()
    if "message" in job.meta:
        message: str = job.meta["message"]
        return message
    else:
        return None


def get_position_in_detailed_queue(athlete_id: int) -> Optional[int]:
    """
    Returns 1 if you're first in line, and 2 if you're second in line, etc.
    Returns None if you're not in the queue at all.
    """
    queued_jobs = detailed_queue.job_ids
    try:
        position = queued_jobs.index(get_detailed_job_id(athlete_id)) + 1
        return position
    except ValueError:
        return None  # Job not found in the queue


def get_position_in_summary_queue(athlete_id: int) -> Optional[int]:
    """
    Returns 1 if you're first in line, and 2 if you're second in line, etc.
    Returns None if you're not in the queue at all.
    """
    queued_jobs = summary_queue.job_ids
    try:
        position = queued_jobs.index(get_summary_job_id(athlete_id)) + 1
        return position
    except ValueError:
        return None  # Job not found in the queue


def get_detailed_job_id(athlete_id: int) -> str:
    return f"{athlete_id}_detailed"


def get_summary_job_id(athlete_id: int) -> str:
    return f"{athlete_id}_summary"
