from decimal import Decimal

from pydantic import BaseModel

from app.models.warehouse import Unit


class RawMaterialBase(BaseModel):
    name: str
    unit: Unit
    min_stock: Decimal


# CREATE


class RawMaterialCreate(RawMaterialBase):
    one_price: Decimal


class RawMaterialCreateStore(RawMaterialBase):
    pass


# UPDATE


class RawMaterialUpdate(RawMaterialBase):
    one_price: Decimal


class RawMaterialUpdateStore(BaseModel):
    name: str | None = None
    unit: Unit | None = None
    min_stock: Decimal | None = None


# RESPONSE


class RawMaterialResponse(RawMaterialBase):
    one_price: Decimal | None
    current_stock: Decimal
    model_config = {"from_attributes": True}


class RawMaterialResponseStore(RawMaterialBase):
    current_stock: Decimal
    model_config = {"from_attributes": True}
