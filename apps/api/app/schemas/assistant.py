from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.destination import DestinationOut


class TripPlanRequest(BaseModel):
    origin: str = Field(min_length=2, max_length=220)
    region: str = Field(default="", max_length=160)
    budget: float = Field(gt=0, le=100_000_000)
    budgetType: Literal["total", "per-person"] = "total"
    travelers: int = Field(default=1, ge=1, le=30)
    duration: Literal["day", "weekend", "multi-day"] = "day"
    interests: list[str] = Field(default_factory=list, max_length=20)

    @field_validator("origin", "region")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class BudgetAnalysis(BaseModel):
    supplied_budget: float
    effective_group_budget: float
    currency: str = "INR"
    estimate_status: Literal["insufficient_cost_data", "estimate_available"]
    note: str


class TripPlanResponse(BaseModel):
    mode: Literal["live", "fallback"]
    message: str
    suggested: list[DestinationOut]
    sources: list[dict] = Field(default_factory=list)
    budget_analysis: BudgetAnalysis
    warnings: list[str] = Field(default_factory=list)
