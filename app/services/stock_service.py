from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.user import User
from app.models.warehouse import OperationType, RawMaterial, StockOperation
from app.schemas.stock_operation import StockOperationCreate


class StockService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_material_for_update(self, raw_material_id: int) -> RawMaterial:
        result = await self.db.execute(select(RawMaterial).where(RawMaterial.id == raw_material_id).with_for_update())
        raw_material: RawMaterial | None = result.scalar_one_or_none()

        if raw_material is None:
            raise NotFoundError("Raw material not found")
        return raw_material

    async def _create_operation_and_commit(
        self, data: StockOperationCreate, user: User, operation_type: OperationType
    ) -> StockOperation:
        operation = StockOperation(
            raw_material_id=data.raw_material_id,
            quantity=data.quantity,
            operation_type=operation_type,
            user_id=user.id,
            comment=data.comment,
        )
        self.db.add(operation)
        await self.db.commit()
        await self.db.refresh(operation)

        return operation

    async def create_income(self, data: StockOperationCreate, user: User) -> StockOperation:
        material = await self._get_material_for_update(data.raw_material_id)
        material.current_stock += data.quantity

        return await self._create_operation_and_commit(data, user, OperationType.PRIHOD)

    async def create_expense(self, data: StockOperationCreate, user: User) -> StockOperation:
        material = await self._get_material_for_update(data.raw_material_id)

        if material.current_stock < data.quantity:
            raise ConflictError(
                f"Not enough material in stock: available {material.current_stock}, requested {data.quantity}"
            )
        material.current_stock -= data.quantity

        return await self._create_operation_and_commit(data, user, OperationType.RASHOD)

    async def create_return_material(self, data: StockOperationCreate, user: User) -> StockOperation:
        material = await self._get_material_for_update(data.raw_material_id)

        material.current_stock += data.quantity

        return await self._create_operation_and_commit(data, user, OperationType.VOZVRAT)

    async def list_operations(
        self,
        raw_material_id: int | None = None,
        operation_type: OperationType | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[StockOperation]:
        query = select(StockOperation)

        if raw_material_id is not None:
            query = query.where(
                StockOperation.raw_material_id == raw_material_id,
            )
        if operation_type is not None:
            query = query.where(
                StockOperation.operation_type == operation_type,
            )

        if date_from is not None:
            query = query.where(
                StockOperation.created_at >= date_from,
            )
        if date_to is not None:
            query = query.where(
                StockOperation.created_at <= date_to,
            )
        query = (
            query.order_by(
                StockOperation.created_at.desc(),
                StockOperation.id.desc(),
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(query)

        return list(result.scalars().all())
