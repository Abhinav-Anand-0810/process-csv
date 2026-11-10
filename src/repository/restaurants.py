"""
Repository handeling DB communications for for Menu Items.
"""

from google.cloud.firestore import Transaction

from enums import FirestoreCollections
from settings import FS_CLIENT


class RestaurantRepository:
    """
    Handels DB operations for Restaurants
    """

    def __init__(self) -> None:
        """
        Initializes the Repository class
        """

        self.db = FS_CLIENT

    def is_restaurant_present(
        self, restaurant_id: str, transaction: Transaction | None = None
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
            self.db.document(
                f"{FirestoreCollections.RESTAURANTS.value}/{restaurant_id}"
            )
            .get(transaction=transaction)
            .exists
        )
