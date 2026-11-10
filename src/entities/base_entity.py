"""
Schemas for Base entity model
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """
    Base Entity Model for common fields
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")), alias="_createdAt"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")), alias="_updatedAt"
    )
