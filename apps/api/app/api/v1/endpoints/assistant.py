from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assistant import TripPlanRequest, TripPlanResponse
from app.services.assistant import plan_trip

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/plan", response_model=TripPlanResponse)
async def create_plan(payload: TripPlanRequest, db: Session = Depends(get_db)) -> TripPlanResponse:
    result = await plan_trip(db, payload)
    return TripPlanResponse.model_validate(result)
