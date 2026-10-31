import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, JSON, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    origin: Mapped[str] = mapped_column(String(220), nullable=False)
    region: Mapped[str] = mapped_column(String(160), default="", nullable=False)
    budget: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    budget_type: Mapped[str] = mapped_column(String(20), nullable=False)
    travelers: Mapped[int] = mapped_column(nullable=False)
    duration: Mapped[str] = mapped_column(String(20), nullable=False)
    interests: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    itinerary: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    estimated_total: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(24), default="draft", index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
