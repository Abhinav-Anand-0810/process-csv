"""
Entry Point for the Job Trigger
"""

import logging

from google.cloud.exceptions import NotFound
from pydantic import ValidationError

from enums import ErrorMessage
from exceptions import AlreadyExistsException, NotFoundException
from schemas.dtos import MenuItemDTO
from settings import (
    SEND_NOTIFICATION_TOPIC,
    UPLOADED_BUCKET_NAME,
    UPLOADED_BY,
    UPLOADED_FILE_NAME,
)
from src.services.menu_items import MenuItemService
from utils.pub_sub import publish
from utils.storage import read_csv

logger = logging.getLogger(__name__)


def process_csv() -> None:
    """
    Validates Menu Items from CSV File and inserts the items in the firestore
    """

    logger.info("Process CSV File Job Started...")

    success_count = 0
    failure_count = 0

    try:
        # Process each item
        csv_rows = read_csv(bucket=UPLOADED_BUCKET_NAME, file=UPLOADED_FILE_NAME)
        menu_item_service = MenuItemService()

        for row in csv_rows:
            try:
                validated_menu_item = MenuItemDTO(**row)

                # Insert Item in DB
                if menu_item_service.create_menu_item(
                    validated_menu_item=validated_menu_item
                ):
                    success_count += 1

            except (
                ValidationError,
                NotFoundException,
                AlreadyExistsException,
            ) as error:
                failure_count += 1
                logger.warning(str(error))

        # Publish Final Results
        publish(
            topic=SEND_NOTIFICATION_TOPIC,
            data={
                "user_email": UPLOADED_BY,
                "subject": "File processed successfully.",
                "body": f"Uploaded file {UPLOADED_FILE_NAME} was processed successfully. Total Items Updated: {success_count}. Failed to process {failure_count} items.",
            },
        )
        logger.info("Operation Completed Successfully.")

    except NotFound:
        logger.warning("File Not Found")
        publish(
            topic=SEND_NOTIFICATION_TOPIC,
            data={
                "user_email": UPLOADED_BY,
                "subject": ErrorMessage.FILE_NOT_FOUND.value,
                "body": f"File {UPLOADED_FILE_NAME} does not exists.",
            },
        )


if __name__ == "__main__":
    process_csv()
