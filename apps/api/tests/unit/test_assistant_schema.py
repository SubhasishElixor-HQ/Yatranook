import pytest
from pydantic import ValidationError

from app.schemas.assistant import TripPlanRequest


def test_small_positive_budget_is_valid():
    request = TripPlanRequest(origin="Bhubaneswar", region="Odisha", budget=150, travelers=1, duration="day")
    assert request.budget == 150


def test_zero_budget_is_invalid():
    with pytest.raises(ValidationError):
        TripPlanRequest(origin="Bhubaneswar", budget=0)


def test_per_person_budget_is_distinguished():
    request = TripPlanRequest(origin="Bhubaneswar", budget=1000, budgetType="per-person", travelers=3)
    assert request.budgetType == "per-person"
    assert request.travelers == 3
