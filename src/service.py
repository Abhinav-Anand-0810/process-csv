"""
Service layer handeling business logic
"""

from google.cloud import firestore

from enums import ErrorMessage
from exceptions import AlreadyExistsException, NotFoundException
from schemas.menu_items import MenuItemDTO, MenuItemEntity
from src.repository import MenuItemRepository


class MenuItemService:
    """
    Business Logic related to Menu Items
    """

    def __init__(self) -> None:
        """
        Initializes the service class
        """

        self.repository = MenuItemRepository()

    def create_menu_item(self, item_dto: MenuItemDTO) -> bool:
        """
        Creates a DB transaction and executes the menu item insertion workflow to prevent race conditions

        Args:
            item_dto: MenuItemDTO Object

        Returns:
            True if the item is inserted successfully
        """

        @firestore.transactional
        def _execute_in_transaction(
            transaction: firestore.Transaction, dto: MenuItemDTO
        ) -> bool:
            # Verify if the restaurant exists
            if not self.repository.is_restaurant_present(
                restaurant_id=dto.restaurant_id, transaction=transaction
            ):
                raise NotFoundException(message=ErrorMessage.RESTAURANT_NOT_FOUND.value)

            # Verify that the menu item does not already exists
            if self.repository.is_menu_item_present(
                restaurant_id=dto.restaurant_id,
                item_name=dto.name,
                transaction=transaction,
            ):
                raise AlreadyExistsException(
                    message=ErrorMessage.MENU_ITEM_ALREADY_EXISTS.value
                )

            # Build Entity Payload
            entity = MenuItemEntity.from_dto(item=item_dto)
            payload = entity.model_dump(by_alias=True)

            # Insert the menu Item
            self.repository.insert_menu_item(
                restaurant_id=dto.restaurant_id,
                payload=payload,
                transaction=transaction,
            )
            return True

        transaction = self.repository.create_transaction()
        return _execute_in_transaction(transaction, item_dto)
