from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.destination import Destination
from app.schemas.destination import DestinationOut

router = APIRouter(prefix="/destinations", tags=["destinations"])


@router.get("", response_model=list[DestinationOut])
def list_destinations(
    search: str = Query(default="", max_length=160),
    region: str | None = Query(default=None, max_length=120),
    category: str | None = Query(default=None, max_length=40),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[DestinationOut]:
    statement = select(Destination)
    if search.strip():
        pattern = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                Destination.name.ilike(pattern),
                Destination.location.ilike(pattern),
                Destination.description.ilike(pattern),
                Destination.category.ilike(pattern),
            )
        )
    if region:
        statement = statement.where(Destination.region.ilike(f"%{region.strip()}%"))
    if category:
        statement = statement.where(Destination.category.ilike(category.strip()))
    items = db.scalars(statement.order_by(Destination.name).limit(limit)).all()
    return [DestinationOut.from_model(item) for item in items]


@router.get("/{destination_id}", response_model=DestinationOut)
def get_destination(destination_id: str, db: Session = Depends(get_db)) -> DestinationOut:
    item = db.get(Destination, destination_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return DestinationOut.from_model(item)
