from fastapi import APIRouter

from app.api.v1.endpoints import warehouse

api_router = APIRouter()

api_router.include_router(warehouse.router, prefix="/warehouse", tags=["warehouse"])
