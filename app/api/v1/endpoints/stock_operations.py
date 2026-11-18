from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_role
from app.db.session import get_db
from app.models import UserRole
from app.models.user import User
from app.schemas.stock_operation import StockOperationCreate, StockOperationResponse
from app.services.stock_service import create_income

router = APIRouter()


@router.post(
    "/operations/income",
    response_model=StockOperationResponse,
    status_code=201,
)
async def income(
    data: StockOperationCreate,
    current_user: Annotated[User, Depends(require_role(UserRole.STOREKEEPER))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await create_income(data, current_user, db)
