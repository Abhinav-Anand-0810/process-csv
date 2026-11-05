"""
Entry Point which executes on Job Trigger
"""

import logging

from google.cloud.exceptions import NotFound
from pydantic import ValidationError

from enums import ErrorMessage
from schemas.menu_items import MenuItem
from settings import UPLOADED_BUCKET_NAME, UPLOADED_FILE_NAME
from utils import firestore, pub_sub, storage

logger = logging.getLogger(__name__)


def process_csv() -> None:
    """
    Validates Menu Items from CSV File and inserts the items in the firestore
    """

    logger.info("Process CSV File Job Started...")

    success_count = 0
    failure_count = 0
    existing_restaurants = set()
    non_existing_restaurants = set()

    try:
        # Process each item
        csv_rows = storage.read_csv(
            bucket=UPLOADED_BUCKET_NAME, file=UPLOADED_FILE_NAME
        )
        for row in csv_rows:
            try:
                item = MenuItem(**row)
                item.name = item.name.lower()

                # Check if restaurant exists
                if item.restaurant_id in non_existing_restaurants:
                    failure_count += 1
                    continue
                if item.restaurant_id not in existing_restaurants:
                    if not firestore.check_restaurant_exists(
                        restaurant_id=item.restaurant_id
                    ):
                        non_existing_restaurants.add(item.restaurant_id)
                        failure_count += 1
                        continue
                    else:
                        existing_restaurants.add(item.restaurant_id)

                # Insert Item in DB
                is_successfull = firestore.insert_menu_item(item=item)
                if is_successfull:
                    success_count += 1
                else:
                    failure_count += 1

            except ValidationError:
                failure_count += 1

        # Publish Final Results
        pub_sub.publish(
            data={
                "message": "Operation Completed",
                "success_count": success_count,
                "failure_count": failure_count,
            }
        )
        logger.info("Operation Completed Successfully.")

    except NotFound:
        logger.info("File Not Found")
        pub_sub.publish(data={"message": ErrorMessage.FILE_NOT_FOUND.value})


if __name__ == "__main__":
    process_csv()
