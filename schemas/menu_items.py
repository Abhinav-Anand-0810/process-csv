"""
Schemas for the project
"""

from typing import Any

from google.cloud import firestore
from pydantic import BaseModel, ConfigDict, Field, field_validator


class MenuItemDTO(BaseModel):
    """
    Schema for Menu Items recieved via input
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    restaurant_id: str = Field(min_length=3)
    name: str = Field(min_length=3)
    rate: float = Field(gt=0)
    quantity: int = Field(gt=0)

    @field_validator("name", mode="after")
    @classmethod
    def lowercase_name(cls, value: str) -> str:
        """
        Converts name to lowercase

        Args:
            value: Input String Value

        Returns:
            Input string converted to lowercase
        """

        return value.lower()


class MenuItemEntity(BaseModel):
    """
    Database Schema for Menu Items
    """

    name: str = Field(min_length=3)
    rate: float = Field(gt=0)
    quantity: int = Field(gt=0)
    created_at: Any | None = Field(default=None, serialization_alias="_created_at")
    updated_at: Any | None = Field(default=None, serialization_alias="_updated_at")

    @classmethod
    def from_dto(cls, item: MenuItemDTO):
        """
        For initalizing Menu Item Entity Object

        Args:
            item: MenuItemDTO Object
        """

        return cls(
            name=item.name,
            rate=item.rate,
            quantity=item.quantity,
            created_at=firestore.SERVER_TIMESTAMP,
            updated_at=firestore.SERVER_TIMESTAMP,
        )
