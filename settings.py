"""
Common configurations for the project
"""

import os

import google.cloud.logging
from google.cloud import firestore, pubsub_v1, storage

# Logger Config
LOGGING_CLIENT = google.cloud.logging.Client()
LOGGING_CLIENT.setup_logging()

# Environment Variables
GCP_PROJECT = os.environ.get("GCP_PROJECT")
PUBSUB_UPLOAD_CSV_TOPIC_ID = os.environ.get("PUBSUB_UPLOAD_CSV_TOPIC_ID")
DATABASE_ID = os.environ.get("DATABASE_ID")
UPLOADED_BUCKET_NAME = os.environ.get("UPLOADED_BUCKET_NAME")
UPLOADED_FILE_NAME = os.environ.get("UPLOADED_FILE_NAME")

# Firestore Config
FIRESTORE_DB = firestore.Client(database=DATABASE_ID)

# PubSub Config
PUBSUB_CLIENT = pubsub_v1.PublisherClient()
BULK_MENU_ITEMS_PUBSUB_TOPIC = PUBSUB_CLIENT.topic_path(
    GCP_PROJECT, PUBSUB_UPLOAD_CSV_TOPIC_ID
)

# Storage Config
STORAGE_CLIENT = storage.Client()
