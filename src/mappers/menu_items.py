"""
Mappers for Menu Items
"""

from src.dtos.menu_items import MenuItemDTO
from src.entities.menu_items import MenuItemEntity


class MenuItemMapper:
    """
    Mapper class to handel conversions between DTO and Entity objects
    """

    @staticmethod
    def to_entity(dto: MenuItemDTO) -> MenuItemEntity:
        """
        Maps MenuItemDTO Object to MenuItemEntity Object

        Args:
            dto: MenuItemDTO Object

        Returns:
            MenuItemEntity object
        """

        return MenuItemEntity(name=dto.name, rate=dto.rate, quantity=dto.quantity)
