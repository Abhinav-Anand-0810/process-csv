"""
Schemas for Base entity model
"""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """
    Base Entity Model for common fields
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), alias="_createdAt"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), alias="_updatedAt"
    )
