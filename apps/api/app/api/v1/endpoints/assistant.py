from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assistant import TripChatRequest, TripChatResponse, TripPlanRequest, TripPlanResponse
from app.services.assistant import chat_trip, plan_trip

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/plan", response_model=TripPlanResponse)
async def create_plan(payload: TripPlanRequest, db: Session = Depends(get_db)) -> TripPlanResponse:
    result = await plan_trip(db, payload)
    return TripPlanResponse.model_validate(result)


@router.post("/chat", response_model=TripChatResponse)
async def chat(payload: TripChatRequest, db: Session = Depends(get_db)) -> TripChatResponse:
    result = await chat_trip(db, payload)
    return TripChatResponse.model_validate(result)
