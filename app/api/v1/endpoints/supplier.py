from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_role
from app.db.session import get_db
from app.models import UserRole
from app.models.user import User
from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)
from app.services.supplier_service import (
    create_supplier,
    delete_supplier,
    get_supplier,
    list_suppliers,
    update_supplier,
)

router = APIRouter()


@router.post(
    "/suppliers",
    response_model=SupplierResponse,
    status_code=201,
)
async def supplier_create(
    data: SupplierCreate,
    current_user: Annotated[User, Depends(require_role(UserRole.OWNER))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await create_supplier(data, db)


@router.get(
    "/suppliers",
    response_model=list[SupplierResponse],
)
async def suppliers_get(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await list_suppliers(db)


@router.get(
    "/suppliers/{supplier_id}",
    response_model=SupplierResponse,
)
async def supplier_get(
    supplier_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await get_supplier(supplier_id, db)


@router.patch(
    "/suppliers/{supplier_id}",
    response_model=SupplierResponse,
)
async def supplier_update(
    supplier_id: int,
    data: SupplierUpdate,
    current_user: Annotated[User, Depends(require_role(UserRole.OWNER))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await update_supplier(supplier_id, data, db)


@router.delete("/suppliers/{supplier_id}", status_code=204)
async def supplier_delete(
    supplier_id: int,
    current_user: Annotated[User, Depends(require_role(UserRole.OWNER))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await delete_supplier(supplier_id, db)
