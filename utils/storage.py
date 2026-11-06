"""
Utilities related to google cloud storage.
"""

import csv
import logging

from settings import STORAGE_CLIENT

logger = logging.getLogger(__name__)


def read_csv(bucket: str, file: str):
    """
    Streams Data from CSV File

    Args:
        bucket: Cloud Storage Bucket Name
        file: Name of the file in the Bucket

    Returns:
        Generator for reading csv file data row by row
    """

    logger.info("Reading CSV File...")
    bucket_obj = STORAGE_CLIENT.bucket(bucket)
    blob = bucket_obj.blob(file)

    with blob.open("r", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]
        yield from reader


def get_uploader_email(bucket: str, file: str) -> str | None:
    """
    Fetches and returns the email of the user who uploaded the file

    Args:
        bucket: Cloud Storage Bucket Name
        file: Name of the file in the Bucket

    Returns:
        Email of the user who uploaded the file
    """

    logger.info("Fetching user email...")

    blob = STORAGE_CLIENT.bucket(bucket).get_blob(file)
    if not blob:
        return None

    blob.reload(projection="full")
    if blob.owner and "entity" in blob.owner:
        return blob.owner["entity"].removeprefix("user-")
    return None
