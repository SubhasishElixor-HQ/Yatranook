import asyncio

from app.schemas.routes import RouteStopInput
from app.services.routing import geographic_nearest_neighbor, haversine_km, optimize_route
from app.schemas.routes import RouteOptimizeRequest


def test_haversine_same_point_is_zero():
    point = RouteStopInput(id="a", name="A", latitude=20.0, longitude=85.0)
    assert haversine_km(point, point) == 0


def test_nearest_neighbor_orders_closer_stop_first():
    origin = RouteStopInput(id="origin", name="Origin", latitude=20.0, longitude=85.0)
    near = RouteStopInput(id="near", name="Near", latitude=20.01, longitude=85.0)
    far = RouteStopInput(id="far", name="Far", latitude=21.0, longitude=85.0)
    ordered = geographic_nearest_neighbor(origin, [far, near])
    assert [item.id for item in ordered] == ["near", "far"]


def test_route_preview_does_not_claim_road_distance_without_provider():
    payload = RouteOptimizeRequest(
        origin=RouteStopInput(id="origin", name="Origin", latitude=20.0, longitude=85.0),
        stops=[RouteStopInput(id="a", name="A", latitude=20.1, longitude=85.0)],
        mode="balanced",
    )
    result = asyncio.run(optimize_route(payload))
    assert result.status == "geographic_order_preview"
    assert result.road_distance_km is None
    assert result.duration_minutes is None
    assert any("Straight-line distance" in item for item in result.limitations)
