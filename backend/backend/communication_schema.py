"""
A file that defines messages sent between the front-end and the backend.
"""

import dataclasses


@dataclasses.dataclass
class DataStatusMessage:
    """
    The message response sent to the client when it calls either of the data
    status endpoints to get information about whether the user has data.
    """

    message: str
    downloaded: bool


@dataclasses.dataclass
class RefreshStatusMessage:
    """
    A server response to the request to refresh data.
    """

    message: str
    refresh_accepted: bool
