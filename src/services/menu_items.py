"""
Service layer handeling business logic related to Menu Items
"""

from google.cloud import firestore

from exceptions import AlreadyExistsException, NotFoundException
from mappers.menu_items import MenuItemMapper
from schemas.dtos import MenuItemDTO
from src.repository.menu_items import MenuItemRepository
from src.repository.restaurants import RestaurantRepository


class MenuItemService:
    """
    Business Logic related to Menu Items
    """

    def __init__(self) -> None:
        """
        Initializes the service class
        """

        self.menu_items_repo = MenuItemRepository()
        self.restaurant_repo = RestaurantRepository()

    def create_menu_item(self, validated_menu_item: MenuItemDTO) -> bool:
        """
        Creates a DB transaction and executes the menu item insertion workflow to prevent race conditions

        Args:
            validated_menu_item: MenuItemDTO Object

        Returns:
            True if the item is inserted successfully
        """

        @firestore.transactional
        def _execute_in_transaction(
            transaction: firestore.Transaction, validated_menu_item: MenuItemDTO
        ) -> bool:
            # Verify if the restaurant exists
            if not self.restaurant_repo.is_restaurant_present(
                restaurant_id=validated_menu_item.restaurant_id, transaction=transaction
            ):
                raise NotFoundException(message="Restaurant not found")

            # Verify that the menu item does not already exists
            if self.menu_items_repo.is_menu_item_present(
                restaurant_id=validated_menu_item.restaurant_id,
                item_name=validated_menu_item.name,
                transaction=transaction,
            ):
                raise AlreadyExistsException(
                    message=f"Item {validated_menu_item.name} already exists."
                )

            # Build Entity Payload
            entity = MenuItemMapper.to_entity(dto=validated_menu_item)
            payload = entity.model_dump(by_alias=True)

            # Insert the menu Item
            self.menu_items_repo.insert_menu_item(
                restaurant_id=validated_menu_item.restaurant_id,
                payload=payload,
                transaction=transaction,
            )
            return True

        transaction = self.menu_items_repo.create_transaction()
        return _execute_in_transaction(transaction, validated_menu_item)
