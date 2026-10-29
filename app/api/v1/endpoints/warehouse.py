from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_role
from app.db.session import get_db
from app.models import UserRole
from app.models.user import User

# from app.models.warehouse import RawMaterial
from app.schemas.warehouse import (
    RawMaterialCreate,
    RawMaterialCreateStore,
    RawMaterialResponse,
    RawMaterialResponseStore,
    RawMaterialUpdate,
    RawMaterialUpdateStore,
)
from app.services.warehouse_service import (
    create_raw_material,
    delete_raw_material,
    get_raw_material,
    list_raw_materials,
    update_raw_material,
)

router = APIRouter()


# Для владельца
@router.post(
    "/raw-materials",
    response_model=RawMaterialResponse,
    status_code=201,
)
async def create_material(
    data: RawMaterialCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await create_raw_material(data, db)


# Для кладовщика
@router.post(
    "/raw-materials/store",
    response_model=RawMaterialResponseStore,
    status_code=201,
)
async def create_material_store(
    data: RawMaterialCreateStore,
    current_user: Annotated[User, Depends(require_role(UserRole.STOREKEEPER))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await create_raw_material(data, db)


@router.get("/raw-materials/{name}")
async def get_material(
    material_name: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    material = await get_raw_material(material_name, db)
    if current_user.role in {
        UserRole.OWNER,
        UserRole.CHIEF_ACCOUNTANT,
    }:
        return RawMaterialResponse.model_validate(material)
    else:
        return RawMaterialResponseStore.model_validate(material)


@router.get(
    "/raw-materials",
    response_model=list[RawMaterialResponse] | list[RawMaterialResponseStore],
)
async def get_materials(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    materials = await list_raw_materials(db)

    if current_user.role in {
        UserRole.OWNER,
        UserRole.CHIEF_ACCOUNTANT,
    }:
        return [RawMaterialResponse.model_validate(material) for material in materials]

    return [RawMaterialResponseStore.model_validate(material) for material in materials]


@router.patch(
    "/raw-materials/{name}",
    response_model=RawMaterialResponse,
)
async def update_material(
    name: str,
    data: RawMaterialUpdate,
    current_user: Annotated[
        User,
        Depends(
            require_role(
                UserRole.OWNER,
                UserRole.CHIEF_ACCOUNTANT,
            )
        ),
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await update_raw_material(name, data, db)


@router.patch(
    "/raw-materials/{name}/store",
    response_model=RawMaterialResponseStore,
)
async def update_material_store(
    name: str,
    data: RawMaterialUpdateStore,
    current_user: Annotated[User, Depends(require_role(UserRole.STOREKEEPER))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await update_raw_material(name, data, db)


@router.delete(
    "/raw-materials/{name}",
    status_code=204,
)
async def delete_material(
    name: str,
    current_user: Annotated[User, Depends(require_role(UserRole.OWNER))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await delete_raw_material(name, db)
