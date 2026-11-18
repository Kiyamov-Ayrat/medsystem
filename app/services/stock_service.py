from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.user import User
from app.models.warehouse import OperationType, RawMaterial, StockOperation
from app.schemas.stock_operation import StockOperationCreate


async def create_income(data: StockOperationCreate, user: User, db: AsyncSession) -> StockOperation:
    res_material = await db.execute(select(RawMaterial).where(RawMaterial.id == data.raw_material_id).with_for_update())
    material = res_material.scalar_one_or_none()

    if material is None:
        raise NotFoundError("Raw material not found")

    stock = data.quantity + material.current_stock

    operation = StockOperation(
        raw_material_id=data.raw_material_id,
        operation_type=OperationType.PRIHOD,
        quantity=data.quantity,
        comment=data.comment,
        user_id=user.id,
    )

    material.current_stock = stock

    db.add(operation)
    await db.commit()
    await db.refresh(operation)
    return operation
