from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import AwareDatetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_role
from app.db.session import get_db
from app.models import UserRole
from app.models.user import User
from app.models.warehouse import OperationType
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


@router.get(
    "/operations",
    response_model=list[StockOperationResponse],
    status_code=200,
)
async def get_list_operations(
    current_user: Annotated[User, Depends(get_current_user)],
    stock_service: Annotated[StockService, Depends(get_stock_service)],
    raw_material_id: int | None = None,
    operation_type: OperationType | None = None,
    date_from: AwareDatetime | None = None,
    date_to: AwareDatetime | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return await stock_service.list_operations(
        raw_material_id=raw_material_id,
        operation_type=operation_type,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )
