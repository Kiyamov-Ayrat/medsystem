from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.warehouse import OperationType


class StockOperationBase(BaseModel):
    pass


class StockOperationCreate(StockOperationBase):
    raw_material_id: int
    quantity: Decimal = Field(gt=0, max_digits=10, decimal_places=3)
    comment: str | None = Field(
        default=None,
        max_length=255,
    )


class StockOperationResponse(StockOperationBase):
    id: int
    comment: str | None = None
    quantity: Decimal
    raw_material_id: int
    operation_type: OperationType
    created_at: datetime
    user_id: int
    model_config = {"from_attributes": True}
