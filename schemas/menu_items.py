"""
Schema for CSV File data validations
"""

from pydantic import BaseModel, ConfigDict, Field


class MenuItem(BaseModel):
    """
    Schema for Menu Items
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    restaurant_id: str = Field(min_length=3)
    name: str = Field(min_length=3)
    rate: float = Field(gt=0)
    quantity: int = Field(gt=0)
