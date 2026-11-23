from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_role
from app.db.session import get_db
from app.models import UserRole
from app.models.user import User
from app.schemas.stock_operation import StockOperationCreate, StockOperationResponse
from app.services.stock_service import StockService

router = APIRouter()


def get_stock_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StockService:
    return StockService(db)


@router.post(
    "/operations/income",
    response_model=StockOperationResponse,
    status_code=201,
)
async def income(
    data: StockOperationCreate,
    current_user: Annotated[User, Depends(require_role(UserRole.STOREKEEPER))],
    stock_service: Annotated[StockService, Depends(get_stock_service)],
):
    return await stock_service.create_income(data, current_user)


@router.post(
    "/operations/expense",
    response_model=StockOperationResponse,
    status_code=201,
)
async def expense(
    data: StockOperationCreate,
    current_user: Annotated[User, Depends(require_role(UserRole.STOREKEEPER))],
    stock_service: Annotated[StockService, Depends(get_stock_service)],
):
    return await stock_service.create_expense(data, current_user)


@router.post(
    "/operations/return",
    response_model=StockOperationResponse,
    status_code=201,
)
async def return_material(
    data: StockOperationCreate,
    current_user: Annotated[User, Depends(require_role(UserRole.STOREKEEPER))],
    stock_service: Annotated[StockService, Depends(get_stock_service)],
):
    return await stock_service.create_return_material(data, current_user)
