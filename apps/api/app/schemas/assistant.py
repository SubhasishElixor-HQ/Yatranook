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


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class TripChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    origin: str = Field(default="", max_length=220)
    region: str = Field(default="", max_length=160)
    budget: float | None = Field(default=None, gt=0, le=100_000_000)
    budgetType: Literal["total", "per-person"] = "total"
    travelers: int = Field(default=1, ge=1, le=30)
    duration: Literal["day", "weekend", "multi-day"] = "day"
    interests: list[str] = Field(default_factory=list, max_length=20)
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)

    @field_validator("message", "origin", "region")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class TripChatResponse(BaseModel):
    mode: Literal["live", "fallback"]
    message: str
    suggested: list[DestinationOut] = Field(default_factory=list)
    sources: list[dict] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
