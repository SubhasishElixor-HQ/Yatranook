from typing import Literal

from pydantic import BaseModel, Field


class RouteStopInput(BaseModel):
    id: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=180)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class RouteOptimizeRequest(BaseModel):
    origin: RouteStopInput
    stops: list[RouteStopInput] = Field(min_length=1, max_length=12)
    mode: Literal["cheapest", "fastest", "shortest", "balanced"] = "balanced"


class RouteOptimizeResponse(BaseModel):
    status: Literal["provider_route", "geographic_order_preview"]
    mode: str
    ordered_stops: list[RouteStopInput]
    straight_line_distance_km: float
    road_distance_km: float | None = None
    duration_minutes: float | None = None
    route_geometry: dict | None = None
    limitations: list[str]
