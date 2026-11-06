"""
Enums for the project
"""

from enum import Enum


class ErrorMessage(str, Enum):
    """
    Enum for Error Messages
    """

    NOT_FOUND = "Resource Not Found."
    RESTAURANT_NOT_FOUND = "Restaurant Not Found."
    FILE_NOT_FOUND = "File Not Found."
    ALREADY_EXISTS = "Resource Already Exists."
    MENU_ITEM_ALREADY_EXISTS = "Menu Item Already Exists."


class FirestoreCollections(str, Enum):
    """
    Enum for Firestore Collections
    """

    RESTAURANT_COLLECTION = "restaurants"
    MENU_ITEMS_SUBCOLLECTION = "menu_items"
