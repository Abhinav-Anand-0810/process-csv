import csv
import logging

from google.cloud import storage

logger = logging.getLogger(__name__)


def read_csv(bucket: str, file: str):
    """
    Streams Data from CSV File
    """
    logger.info("Reading CSV File...")
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(file)

    with blob.open("r", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]
        yield from reader
