from datetime import datetime
from enum import StrEnum

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRole(StrEnum):
    OWNER = "OWNER"
    OFFICE_MANAGER = "OFFICE_MANAGER"
    CHIEF_ACCOUNTANT = "CHIEF_ACCOUNTANT"
    STOREKEEPER = "STOREKEEPER"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(sa.Enum(UserRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
    )
    is_active: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=True)
