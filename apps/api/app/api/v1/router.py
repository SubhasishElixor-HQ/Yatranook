from fastapi import APIRouter

from app.api.v1.endpoints import assistant, auth, destinations, health, routes, trips

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(destinations.router)
api_router.include_router(assistant.router)
api_router.include_router(routes.router)
api_router.include_router(trips.router)
