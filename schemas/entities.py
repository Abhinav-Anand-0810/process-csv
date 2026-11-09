"""
Database Entity Schemas
"""

from schemas.base_entity import BaseEntity


class MenuItemEntity(BaseEntity):
    """
    Database Schema for Menu Items
    """

    name: str
    rate: float
    quantity: int
