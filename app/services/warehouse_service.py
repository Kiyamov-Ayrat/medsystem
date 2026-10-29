from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.warehouse import RawMaterial
from app.schemas.warehouse import (
    RawMaterialCreate,
    RawMaterialCreateStore,
    RawMaterialUpdate,
    RawMaterialUpdateStore,
)


async def create_raw_material(
    data: RawMaterialCreate | RawMaterialCreateStore,
    db: AsyncSession,
) -> RawMaterial:
    material = RawMaterial(**data.model_dump())

    db.add(material)
    await db.flush()
    await db.commit()

    return material


async def get_raw_material(
    raw_material_name: str,
    db: AsyncSession,
) -> RawMaterial:
    result = await db.execute(select(RawMaterial).where(RawMaterial.name == raw_material_name))

    material = result.scalar_one_or_none()

    if material is None:
        raise NotFoundError(f"RawMaterial {raw_material_name} not found")

    return material


async def list_raw_materials(
    db: AsyncSession,
) -> list[RawMaterial]:
    result = await db.execute(select(RawMaterial))

    return list(result.scalars().all())


async def update_raw_material(
    raw_material_name: str,
    data: RawMaterialUpdate | RawMaterialUpdateStore,
    db: AsyncSession,
) -> RawMaterial:
    material = await get_raw_material(
        raw_material_name=raw_material_name,
        db=db,
    )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(material, field, value)

    await db.flush()
    await db.commit()

    return material


async def delete_raw_material(
    material_name: str,
    db: AsyncSession,
) -> None:
    material = await get_raw_material(
        raw_material_name=material_name,
        db=db,
    )

    await db.delete(material)
    await db.flush()
    await db.commit()
