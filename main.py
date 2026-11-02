import logging
import os
import sys

from pydantic import ValidationError

from src.schemas import menu_items
from src.services import firestore, pub_sub, storage

logging.basicConfig(stream=sys.stdout, level=logging.INFO, force=True)
logger = logging.getLogger(__name__)


def process_csv() -> None:
    """
    Validates Menu Items from CSV File and inserts the items in the firestore
    """
    logger.info("Process CSV File Job Started...")

    bucket = os.environ.get("UPLOADED_BUCKET_NAME")
    file = os.environ.get("UPLOADED_FILE_NAME")
    success_count = 0
    failure_count = 0
    existing_restaurants = set()
    non_existing_restaurants = set()

    # Process each item
    for row in storage.read_csv(bucket=bucket, file=file):
        try:
            item = menu_items.MenuItem(**row)
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
    pub_sub.publish(success_count=success_count, failure_count=failure_count)


if __name__ == "__main__":
    try:
        process_csv()
    except Exception:
        logger.exception("Something went wrong...")
