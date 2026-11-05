"""
Common configurations for the project
"""

import logging
import os
import sys

from google.cloud import firestore, pubsub_v1, storage

# Logger Config
logging.basicConfig(stream=sys.stdout, level=logging.INFO, force=True)

# Environment Variables
GCP_PROJECT = os.environ.get("GCP_PROJECT")
PUBSUB_UPLOAD_CSV_TOPIC_ID = os.environ.get("PUBSUB_UPLOAD_CSV_TOPIC_ID")
RESTAURANT_COLLECTION = os.environ.get("RESTAURANT_COLLECTION")
MENU_ITEMS_SUBCOLLECTION = os.environ.get("MENU_ITEMS_SUBCOLLECTION")
DATABASE_ID = os.environ.get("DATABASE_ID")
UPLOADED_BUCKET_NAME = os.environ.get("UPLOADED_BUCKET_NAME")
UPLOADED_FILE_NAME = os.environ.get("UPLOADED_FILE_NAME")

# Firestore Config
FIRESTORE_DB = firestore.Client(database=DATABASE_ID)

# PubSub Config
PUBSUB_CLIENT = pubsub_v1.PublisherClient()
BULK_MENU_ITEMS_PUBLISHER = PUBSUB_CLIENT.topic_path(
    GCP_PROJECT, PUBSUB_UPLOAD_CSV_TOPIC_ID
)

# Storage Config
STORAGE_CLIENT = storage.Client()
