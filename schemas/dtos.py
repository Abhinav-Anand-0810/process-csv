"""
Data Transfer Object Schemas
"""

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
