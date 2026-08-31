from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum

from app.db.base import Base


class UserRole(str, Enum):
    owner = "OWNER"
    office_manager = "OFFICE_MANAGER"
    chief_accountant = "CHIEF_ACCOUNTANT"
    storekeeper = "STOREKEEPER"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    role: Mapped[str] = mapped_column(sa.Enum(UserRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
    )
    is_active: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=True)
