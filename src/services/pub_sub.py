import json
import logging
import os

from google.cloud import pubsub_v1

logger = logging.getLogger(__name__)

PROJECT_ID = os.getenv("GCP_PROJECT")
TOPIC_ID = os.environ.get("PUBSUB_UPLOAD_CSV_TOPIC_ID")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def publish(success_count: int, failure_count: int) -> None:
    """
    Publishes results on Pub/Sub
    """
    logger.info("Publishing results to Pub/Sub")
    message_json = json.dumps(
        {
            "data": {
                "success": success_count,
                "failure": failure_count,
            }
        }
    )
    message_bytes = message_json.encode("utf-8")

    publish_future = publisher.publish(topic_path, data=message_bytes)
    publish_future.result()
    logger.info(
        f"Results Published: Success = {success_count}, Failed = {failure_count}"
    )
