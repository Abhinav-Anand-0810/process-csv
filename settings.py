"""
Common configurations for the project
"""

import os

from google.cloud import firestore, pubsub_v1, storage
from google.cloud.logging_v2.handlers import StructuredLogHandler, setup_logging

# Logger Config
setup_logging(handler=StructuredLogHandler())

# Environment Variables
GCP_PROJECT = os.environ.get("GCP_PROJECT")
SEND_NOTIFICATION_TOPIC_ID = os.environ.get("SEND_NOTIFICATION_TOPIC_ID")
DATABASE_ID = os.environ.get("DATABASE_ID")
UPLOADED_BUCKET_NAME = os.environ.get("UPLOADED_BUCKET_NAME")
UPLOADED_FILE_NAME = os.environ.get("UPLOADED_FILE_NAME")
UPLOADED_BY = os.environ.get("UPLOADED_BY")

# Firestore Config
FS_CLIENT = firestore.Client(database=DATABASE_ID)

# PubSub Config
PUBSUB_CLIENT = pubsub_v1.PublisherClient()
SEND_NOTIFICATION_TOPIC = PUBSUB_CLIENT.topic_path(
    GCP_PROJECT, SEND_NOTIFICATION_TOPIC_ID
)

# Storage Config
STORAGE_CLIENT = storage.Client()
