import math

import httpx

from app.core.config import settings
from app.schemas.routes import RouteOptimizeRequest, RouteOptimizeResponse, RouteStopInput


def haversine_km(a: RouteStopInput, b: RouteStopInput) -> float:
    radius = 6371.0088
    lat1, lon1, lat2, lon2 = map(math.radians, [a.latitude, a.longitude, b.latitude, b.longitude])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    value = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(value))


def geographic_nearest_neighbor(origin: RouteStopInput, stops: list[RouteStopInput]) -> list[RouteStopInput]:
    remaining = list(stops)
    ordered: list[RouteStopInput] = []
    current = origin
    while remaining:
        next_stop = min(remaining, key=lambda stop: haversine_km(current, stop))
        ordered.append(next_stop)
        remaining.remove(next_stop)
        current = next_stop
    return ordered


async def optimize_route(payload: RouteOptimizeRequest) -> RouteOptimizeResponse:
    ordered = geographic_nearest_neighbor(payload.origin, payload.stops)
    sequence = [payload.origin, *ordered]
    straight_line = sum(haversine_km(sequence[index], sequence[index + 1]) for index in range(len(sequence) - 1))
    limitations = [
        "Stop order is a geographical nearest-neighbor preview, not a globally optimal road route.",
        "Straight-line distance is not road distance and must not be used as a directions estimate.",
    ]
    base_url = settings.osrm_base_url
    if base_url and payload.mode != "cheapest":
        coordinates = ";".join(f"{stop.longitude},{stop.latitude}" for stop in sequence)
        url = f"{base_url.rstrip('/')}/route/v1/driving/{coordinates}"
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                response = await client.get(url, params={"overview": "full", "geometries": "geojson", "steps": "false"})
                response.raise_for_status()
                data = response.json()
            route = data.get("routes", [])[0]
            return RouteOptimizeResponse(
                status="provider_route", mode=payload.mode, ordered_stops=ordered,
                straight_line_distance_km=round(straight_line, 2),
                road_distance_km=round(route["distance"] / 1000, 2),
                duration_minutes=round(route["duration"] / 60, 1),
                route_geometry=route.get("geometry"),
                limitations=["OSRM returned a provider-selected driving route for the configured profile; this is not a multi-criteria proof of optimality. Fare comparison is unavailable without current transport fare data."],
            )
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError):
            limitations.append("Configured routing provider was unavailable; returned only a straight-line ordering preview.")
    if payload.mode == "cheapest":
        limitations.append("Cheapest route cannot be established without current transport modes and fare data.")
    elif payload.mode == "fastest":
        limitations.append("Fastest route cannot be established without road-network duration data.")
    elif payload.mode == "shortest":
        limitations.append("Shortest road distance cannot be established without road-network routing data.")
    else:
        limitations.append("Balanced scoring requires reliable road duration and fare inputs; no unsupported score is fabricated.")
    return RouteOptimizeResponse(
        status="geographic_order_preview", mode=payload.mode, ordered_stops=ordered,
        straight_line_distance_km=round(straight_line, 2), limitations=limitations,
    )
