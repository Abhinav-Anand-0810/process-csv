"""
Utility for reading and writing data to Firestore DB
"""

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from schemas.menu_items import MenuItem
from settings import FIRESTORE_DB, MENU_ITEMS_SUBCOLLECTION, RESTAURANT_COLLECTION


def check_restaurant_exists(restaurant_id: str) -> bool:
    """
    Checks if a restaurant exists in the database by ID

    Args:
        restaurant_id: ID of the document in DB

    Returns:
        True if restaurant exists False otherwise
    """

    restaurant_ref = FIRESTORE_DB.collection(RESTAURANT_COLLECTION).document(
        restaurant_id
    )
    restaurant_snap = restaurant_ref.get()
    return restaurant_snap.exists


@firestore.transactional
def insert_menu_item_transaction(
    transaction: firestore.Transaction, item: MenuItem
) -> bool:
    """
    Inserts a menu item in a restaurant

    Args:
        transaction: Firestore Transaction
        item: Menu Item

    Returns:
        True if the item is inserted successfully, False otherwise
    """
    # Check for existing item
    menu_item_ref = (
        FIRESTORE_DB.collection(RESTAURANT_COLLECTION)
        .document(item.restaurant_id)
        .collection(MENU_ITEMS_SUBCOLLECTION)
    )
    query = menu_item_ref.where(
        filter=FieldFilter(field_path="name", op_string="==", value=item.name)
    ).limit(1)
    existing_menu_item = list(query.stream(transaction=transaction))
    if existing_menu_item:
        return False

    # Update Required Fields
    item_dict = item.model_dump(exclude={"restaurant_id"})
    item_dict["_created_at"] = firestore.SERVER_TIMESTAMP
    item_dict["_updated_at"] = firestore.SERVER_TIMESTAMP

    # Insert in DB
    new_item_ref = (
        FIRESTORE_DB.collection(RESTAURANT_COLLECTION)
        .document(item.restaurant_id)
        .collection(MENU_ITEMS_SUBCOLLECTION)
        .document()
    )
    transaction.set(new_item_ref, item_dict)
    return True


def insert_menu_item(item: MenuItem) -> bool:
    """
    Creates a DB Transaction and calls the insert_menu_item_transaction() for handeling race conditions.

    Args:
        item: Menu Item

    Returns:
        True if the item is inserted successfully, False otherwise
    """
    transaction = FIRESTORE_DB.transaction()
    return insert_menu_item_transaction(transaction=transaction, item=item)
