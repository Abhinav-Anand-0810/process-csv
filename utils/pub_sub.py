"""
Utility for publishing results to PubSub
"""

import json
import logging

from settings import BULK_MENU_ITEMS_PUBLISHER, PUBSUB_CLIENT

logger = logging.getLogger(__name__)


def publish(data: dict) -> None:
    """
    Publishes message on Pub/Sub

    Args:
        data: Payload to be published on Pub/Sub
    """

    logger.info("Publishing message to Pub/Sub")
    message_json = json.dumps({"data": data})
    message_bytes = message_json.encode("utf-8")

    publish_future = PUBSUB_CLIENT.publish(
        BULK_MENU_ITEMS_PUBLISHER, data=message_bytes
    )
    publish_future.result()
    logger.info("Message Published")
