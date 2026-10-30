import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TripCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    origin: str = Field(min_length=2, max_length=220)
    region: str = Field(default="", max_length=160)
    budget: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    budget_type: str = Field(default="total", pattern="^(total|per-person)$")
    travelers: int = Field(default=1, ge=1, le=30)
    duration: str = Field(default="day", pattern="^(day|weekend|multi-day)$")
    interests: list[str] = Field(default_factory=list)
    itinerary: dict = Field(default_factory=dict)
    estimated_total: Decimal | None = Field(default=None, ge=0)


class TripOut(TripCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
