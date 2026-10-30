from fastapi import APIRouter

from app.schemas.routes import RouteOptimizeRequest, RouteOptimizeResponse
from app.services.routing import optimize_route

router = APIRouter(prefix="/routes", tags=["routes"])


@router.post("/optimize", response_model=RouteOptimizeResponse)
async def route_optimize(payload: RouteOptimizeRequest) -> RouteOptimizeResponse:
    return await optimize_route(payload)
