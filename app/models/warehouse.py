from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Unit(StrEnum):
    L = "L"
    M = "M"
    SHT = "SHT"
    KG = "KG"
    M_SQR = "M_SQR"
    T = "T"


class OperationType(StrEnum):
    PRIHOD = "PRIHOD"
    RASHOD = "RASHOD"
    VOZVRAT = "VOZVRAT"
    KORREKTIROVKA = "KORREKTIROVKA"


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    contact_info: Mapped[str | None] = mapped_column(sa.String(50), nullable=True)

    raw_materials: Mapped[list["RawMaterial"]] = relationship(
        back_populates="supplier",
    )


class RawMaterial(Base):
    __tablename__ = "raw_materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    unit: Mapped[Unit] = mapped_column(sa.Enum(Unit), nullable=False)
    min_stock: Mapped[Numeric] = mapped_column(sa.Numeric(10, 3), nullable=False)
    current_stock: Mapped[Numeric] = mapped_column(sa.Numeric(10, 3), nullable=False)
    one_price: Mapped[Numeric] = mapped_column(sa.Numeric(10, 3), nullable=False)
    sum_price: Mapped[Numeric] = mapped_column(sa.Numeric(20, 3), nullable=False)

    supplier_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("suppliers.id"),
        nullable=True,
    )

    stock_operations: Mapped[list["StockOperation"]] = relationship(
        back_populates="raw_material",
    )

    supplier: Mapped["Supplier | None"] = relationship(
        back_populates="raw_materials",
    )


class StockOperation(Base):
    __tablename__ = "stock_operations"

    id: Mapped[int] = mapped_column(primary_key=True)
    raw_material_id: Mapped[int] = mapped_column(
        sa.ForeignKey("raw_materials.id"),
        nullable=False,
    )
    operation_type: Mapped[OperationType] = mapped_column(sa.Enum(OperationType), nullable=False)
    quantity: Mapped[Numeric] = mapped_column(sa.Numeric(10, 3), nullable=False)
    comment: Mapped[str | None] = mapped_column(sa.String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
    )

    raw_material: Mapped["RawMaterial"] = relationship(
        back_populates="stock_operations",
    )

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="stock_operations",
    )
