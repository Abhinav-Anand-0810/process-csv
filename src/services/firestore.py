import os

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from src.schemas import menu_items

RESTAURANT_COLLECTION = os.environ.get("RESTAURANT_COLLECTION")
MENU_ITEMS_SUBCOLLECTION = os.environ.get("MENU_ITEMS_SUBCOLLECTION")
DATABASE_ID = os.environ.get("DATABASE_ID")
db = firestore.Client(database=DATABASE_ID)


def check_restaurant_exists(restaurant_id: str) -> bool:
    """
    Checks if a restaurant exists in the database by ID
    """
    restaurant_ref = db.collection(RESTAURANT_COLLECTION).document(restaurant_id)
    restaurant_snap = restaurant_ref.get()
    return restaurant_snap.exists


@firestore.transactional
def insert_menu_item_transaction(
    transaction: firestore.Transaction, item: menu_items.MenuItem
) -> bool:
    """
    Inserts a menu item in a restaurant
    """
    # Check for existing item
    menu_item_ref = (
        db.collection(RESTAURANT_COLLECTION)
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
        db.collection(RESTAURANT_COLLECTION)
        .document(item.restaurant_id)
        .collection(MENU_ITEMS_SUBCOLLECTION)
        .document()
    )
    transaction.set(new_item_ref, item_dict)
    return True


def insert_menu_item(item: menu_items.MenuItem) -> bool:
    """
    Inserts a menu item via a seperate transaction function
    """
    transaction = db.transaction()
    return insert_menu_item_transaction(transaction=transaction, item=item)
