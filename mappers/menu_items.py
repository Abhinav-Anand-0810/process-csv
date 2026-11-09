"""
Mappers for Menu Items
"""

from schemas.dtos import MenuItemDTO
from schemas.entities import MenuItemEntity


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
