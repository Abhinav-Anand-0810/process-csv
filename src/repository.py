"""
Repository handling communication with Firestore Database.
"""

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from enums import FirestoreCollections
from settings import FIRESTORE_DB


class MenuItemRepository:
    """
    Handles Database operations for restaurants and menu items
    """

    def __init__(self) -> None:
        """
        Initializes the Repository class
        """

        self.db = FIRESTORE_DB

    def create_transaction(self) -> firestore.Transaction:
        """
        Initializes and returns a Firestore transaction

        Returns:
            Firestore Transaction
        """

        return self.db.transaction()

    def _get_menu_items_collection(
        self, restaurant_id: str
    ) -> firestore.CollectionReference:
        """
        Helper to build the Menu Item subcollection reference

        Args:
            restaurant_id: ID of the restaurant

        Returns:
            Firestore Collection Reference
        """

        return self.db.collection(
            f"{FirestoreCollections.RESTAURANT_COLLECTION.value}/{restaurant_id}/{FirestoreCollections.MENU_ITEMS_SUBCOLLECTION.value}"
        )

    def is_restaurant_present(
        self, restaurant_id: str, transaction: firestore.Transaction | None = None
    ) -> bool:
        """
        Checks if a restaurant exists

        Args:
            restaurant_id: ID of the restaurant
            transaction: Firestore Transaction, defaults to None

        Returns:
            True if the restaurant exists, False otherwise
        """

        return (
            self.db.collection(FirestoreCollections.RESTAURANT_COLLECTION.value)
            .document(restaurant_id)
            .get(transaction=transaction)
            .exists
        )

    def is_menu_item_present(
        self,
        restaurant_id: str,
        item_name: str,
        transaction: firestore.Transaction | None = None,
    ) -> bool:
        """
        Checks if a menu item with the same name already exists in the restaurant

        Args:
            restaurant_id: ID of the rastaurant
            item_name: Name of the Menu Item
            transaction: Firestore Transaction, defaults to None

        Returns:
            True if the Item already exists, False otherwise
        """

        query = (
            self._get_menu_items_collection(restaurant_id)
            .where(
                filter=FieldFilter(field_path="name", op_string="==", value=item_name)
            )
            .limit(1)
        )
        results = query.get(transaction=transaction)
        return len(results) > 0

    def insert_menu_item(
        self,
        restaurant_id: str,
        payload: dict,
        transaction: firestore.Transaction,
    ) -> None:
        """
        Inserts a new menu item in a restaurnat

        Args:
            restaurant_id: ID of the rastaurant
            payload: Menu Item to be inserted
            transaction: Firestore Transaction
        """

        new_item_ref = self._get_menu_items_collection(restaurant_id).document()
        transaction.set(new_item_ref, payload)
