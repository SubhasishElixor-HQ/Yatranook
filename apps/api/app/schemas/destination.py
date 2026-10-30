from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DestinationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    location: str
    category: str
    description: str
    image: str
    distanceKm: float | None = None
    duration: str | None = None
    priceLabel: str | None = None
    tags: list[str] = Field(default_factory=list)
    latitude: float | None = None
    longitude: float | None = None
    sourceName: str | None = None
    sourceUrl: str | None = None
    verifiedAt: datetime | None = None

    @classmethod
    def from_model(cls, item):
        return cls(
            id=item.id, name=item.name, location=item.location, category=item.category,
            description=item.description, image=item.image, duration=item.duration,
            priceLabel=item.price_label, tags=item.tags or [], latitude=item.latitude,
            longitude=item.longitude, sourceName=item.source_name, sourceUrl=item.source_url,
            verifiedAt=item.verified_at,
        )
