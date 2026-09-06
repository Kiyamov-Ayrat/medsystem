from fastapi import Depends, HTTPException, status

from app.core.config import settings
from app.models.user import User, UserRole


def get_current_user() -> User:
    return User(
        id=1,
        email="dev@example.com",
        hashed_password="",
        full_name="Dev User",
        role=UserRole(settings.dev_fake_user_role),
    )


def require_role(*roles: UserRole):

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user

    return role_checker
