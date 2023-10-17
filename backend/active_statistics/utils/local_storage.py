"""
This file contains all functions to do with data storage.
"""
import os
import pickle
import shutil
from typing import Iterator

from active_statistics.utils.environment_variables import evm
from stravalib.model import Activity

SUMMARY_ACTIVITIES_FILE_NAME = "summary_activities.obj"


def get_athlete_storage_location(athlete_id: int) -> str:
    # Get the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    storage_folder_name = "tmp_storage" if evm.use_s3() else "storage"

    storage_dir = os.path.join(current_dir, "..", storage_folder_name)
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)

    athlete_directory = os.path.join(storage_dir, str(athlete_id))
    if not os.path.exists(athlete_directory):
        os.mkdir(athlete_directory)

    return athlete_directory


def delete_athlete_storage_location(athlete_id: int) -> None:
    """
    Delete the athlete storage location, and everything inside it.
    """
    athlete_directory = get_athlete_storage_location(athlete_id)
    shutil.rmtree(athlete_directory)


def delete_summary_activities(athlete_id: int) -> None:
    athlete_directory = get_athlete_storage_location(athlete_id)

    # Check if the file exists before attempting to delete it
    file_path = os.path.join(athlete_directory, SUMMARY_ACTIVITIES_FILE_NAME)

    if os.path.exists(file_path):
        # Attempt to delete the file
        os.remove(file_path)


def delete_detailed_activities(athlete_id: int) -> None:
    athlete_directory = get_athlete_storage_location(athlete_id)
    # List all files in the directory
    files_in_directory = os.listdir(athlete_directory)

    # Iterate through the files and delete them if they are not the file to keep
    for file_name in files_in_directory:
        if file_name != SUMMARY_ACTIVITIES_FILE_NAME:
            file_path = os.path.join(athlete_directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)


def save_activity_to_file(athlete_id: int, activity: Activity) -> None:
    athlete_storage_location = get_athlete_storage_location(athlete_id)
    activity_file = os.path.join(athlete_storage_location, f"{activity.id}.obj")

    # Replace the bound_client with None, because I don't know what it does,
    # and whenever I change anything with my client, deserializing fails.
    activity.bound_client = None

    # Dump the pickle
    with open(activity_file, "wb") as f:
        pickle.dump(activity, f)


def save_summary_activities_to_file(
    athlete_id: int, activities: list[Activity]
) -> None:
    athlete_storage_location = get_athlete_storage_location(athlete_id)
    activity_file = os.path.join(athlete_storage_location, SUMMARY_ACTIVITIES_FILE_NAME)

    # Replace the bound_client with None, because I don't know what it does,
    # and whenever I change anything with my client, deserializing fails.
    for activity in activities:
        activity.bound_client = None

    # Dump the pickle
    with open(activity_file, "wb") as f:
        pickle.dump(activities, f)


def get_activity_iterator(athlete_id: int) -> Iterator[Activity]:
    """
    Simultaneously loading all detailed athlete activities uses quite a lot of RAM. This is bad because it costs me
    money to buy bigger machines on EC2 to process the data. If I instead iterate over all the activities one at a
    time, I can use far less memory and save money.
    """
    athlete_storage_location = get_athlete_storage_location(athlete_id)
    for f in os.listdir(athlete_storage_location):
        file_path = os.path.join(athlete_storage_location, f)
        if os.path.isfile(file_path) and f != SUMMARY_ACTIVITIES_FILE_NAME:
            with open(file_path, "rb") as fp:
                yield pickle.load(fp)


def get_summary_activity_iterator(athlete_id: int) -> Iterator[Activity]:
    athlete_storage_location = get_athlete_storage_location(athlete_id)
    activity_file = os.path.join(athlete_storage_location, SUMMARY_ACTIVITIES_FILE_NAME)
    if os.path.isfile(activity_file):
        with open(activity_file, "rb") as fp:
            activities = pickle.load(fp)
    for activity in activities:
        yield activity


def we_have_summary_activities_for_athlete(athlete_id: int) -> bool:
    """
    Stolen from ChatGPT this function returns true if there is a single file in the athletes folder.
    """
    athlete_storage_location = get_athlete_storage_location(athlete_id)
    file_path = os.path.join(athlete_storage_location, SUMMARY_ACTIVITIES_FILE_NAME)
    return os.path.isfile(file_path)


def we_have_detailed_activities_for_athlete(athlete_id: int) -> bool:
    """
    Stolen from ChatGPT this function returns true if there is a single file in the athletes folder.
    """
    athlete_storage_location = get_athlete_storage_location(athlete_id)
    for filename in os.listdir(athlete_storage_location):
        if filename != SUMMARY_ACTIVITIES_FILE_NAME and os.path.isfile(
            os.path.join(athlete_storage_location, filename)
        ):
            return True
    return False
