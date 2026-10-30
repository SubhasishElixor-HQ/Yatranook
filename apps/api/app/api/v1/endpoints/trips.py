import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.trip import Trip
from app.models.user import User
from app.schemas.trip import TripCreate, TripOut

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("", response_model=TripOut, status_code=status.HTTP_201_CREATED)
def create_trip(payload: TripCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Trip:
    trip = Trip(user_id=user.id, **payload.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.get("", response_model=list[TripOut])
def list_trips(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[Trip]:
    return list(db.scalars(select(Trip).where(Trip.user_id == user.id).order_by(Trip.updated_at.desc())).all())


@router.get("/{trip_id}", response_model=TripOut)
def get_trip(trip_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Trip:
    trip = db.scalar(select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id))
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> None:
    trip = db.scalar(select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id))
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
