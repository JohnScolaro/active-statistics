import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

SERVER = "SERVER"
TASK = "TASK"


def get_server_log_directory() -> Path:
    log_directory = Path(__file__).parent.resolve() / "logs"
    server_logs_directory = log_directory / "server"
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)
    if not os.path.exists(server_logs_directory):
        os.mkdir(server_logs_directory)
    return server_logs_directory


def get_tasks_log_directory() -> Path:
    log_directory = Path(__file__).parent.resolve() / "logs"
    task_logs_directory = log_directory / "tasks"
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)
    if not os.path.exists(task_logs_directory):
        os.mkdir(task_logs_directory)
    return task_logs_directory


def setup_server_logging() -> None:
    server_logger = logging.getLogger(SERVER)
    server_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler1 = RotatingFileHandler(
        os.path.join(get_server_log_directory(), "server_log.log"),
        maxBytes=200000,
        backupCount=10,
        encoding="utf-8",
    )
    handler1.setFormatter(formatter)

    server_logger.addHandler(handler1)


def setup_task_logging() -> None:
    task_logger = logging.getLogger(TASK)
    task_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler1 = RotatingFileHandler(
        os.path.join(get_tasks_log_directory(), "task_log.log"),
        maxBytes=200000,
        backupCount=10,
        encoding="utf-8",
    )
    handler1.setFormatter(formatter)

    task_logger.addHandler(handler1)
