"""
Utilities related to pub/sub.
"""

import json
import logging

from settings import PUBSUB_CLIENT

logger = logging.getLogger(__name__)


def publish(topic: str, data: dict) -> None:
    """
    Publishes message on Pub/Sub

    Args:
        topic: Pub/Sub topic
        data: Payload to be published on Pub/Sub
    """

    logger.info("Publishing message to Pub/Sub")
    message_bytes = json.dumps({"data": data}).encode("utf-8")

    publish_future = PUBSUB_CLIENT.publish(topic=topic, data=message_bytes)
    publish_future.result()
    logger.info("Message Published")
