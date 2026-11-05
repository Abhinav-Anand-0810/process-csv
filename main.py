"""
Entry Point for the Job Trigger
"""

import logging

from google.cloud.exceptions import NotFound
from pydantic import ValidationError

from enums import ErrorMessage
from exceptions import AlreadyExistsException, NotFoundException
from schemas.menu_items import MenuItemDTO
from settings import (
    BULK_MENU_ITEMS_PUBSUB_TOPIC,
    UPLOADED_BUCKET_NAME,
    UPLOADED_FILE_NAME,
)
from src.service import MenuItemService
from utils import pub_sub, storage

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
        csv_rows = storage.read_csv(
            bucket=UPLOADED_BUCKET_NAME, file=UPLOADED_FILE_NAME
        )
        service = MenuItemService()

        for row in csv_rows:
            try:
                item = MenuItemDTO(**row)

                # Insert Item in DB
                if service.create_menu_item(item_dto=item):
                    success_count += 1
                else:
                    failure_count += 1

            except (
                ValidationError,
                NotFoundException,
                AlreadyExistsException,
            ) as error:
                failure_count += 1
                logger.info(str(error))

        # Publish Final Results
        pub_sub.publish(
            topic=BULK_MENU_ITEMS_PUBSUB_TOPIC,
            data={
                "message": "Operation Completed",
                "success_count": success_count,
                "failure_count": failure_count,
            },
        )
        logger.info("Operation Completed Successfully.")

    except NotFound:
        logger.info("File Not Found")
        pub_sub.publish(
            topic=BULK_MENU_ITEMS_PUBSUB_TOPIC,
            data={"message": ErrorMessage.FILE_NOT_FOUND.value},
        )


if __name__ == "__main__":
    process_csv()
