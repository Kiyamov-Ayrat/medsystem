from fastapi import APIRouter

from app.api.v1.endpoints import supplier, warehouse

api_router = APIRouter()

api_router.include_router(warehouse.router, prefix="/warehouse", tags=["warehouse"])
api_router.include_router(supplier.router, prefix="/warehouse", tags=["supplier"])
