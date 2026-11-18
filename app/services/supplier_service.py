from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.warehouse import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


async def create_supplier(data: SupplierCreate, db: AsyncSession) -> Supplier:

    supplier = Supplier(**data.model_dump())

    db.add(supplier)

    await db.flush()
    await db.commit()

    return supplier


async def get_supplier(supplier_id: int, db: AsyncSession) -> Supplier:
    supplier = await db.get(Supplier, supplier_id)

    if supplier is None:
        raise NotFoundError(f"Supplier {supplier_id} not found")

    return supplier


async def list_suppliers(db: AsyncSession) -> list[Supplier]:
    result = await db.execute(select(Supplier))
    return list(result.scalars().all())


async def update_supplier(supplier_id: int, data: SupplierUpdate, db: AsyncSession) -> Supplier:
    supplier = await get_supplier(
        supplier_id=supplier_id,
        db=db,
    )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "name" and value is None:
            continue
        setattr(supplier, field, value)

    await db.flush()
    await db.commit()

    return supplier


async def delete_supplier(supplier_id: int, db: AsyncSession) -> None:

    supplier = await get_supplier(
        supplier_id=supplier_id,
        db=db,
    )

    try:
        await db.delete(supplier)
        await db.flush()
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ConflictError("Can't delete supplier, it has materials") from exc
