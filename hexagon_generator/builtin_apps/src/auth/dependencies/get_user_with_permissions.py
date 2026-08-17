from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.schemas import AuthUser
from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.domain.exceptions import PermissionDeniedException
from src.auth.infrastructure.database import ORMAuthRepository
from src.common.database_connection import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_auth_use_case(db: AsyncSession = Depends(get_db)) -> AuthUseCase:
    return AuthUseCase(auth_repo=ORMAuthRepository(db=db))


def get_user_with_permission(required_permission: str):
    async def get_current_active_user(
        token: str = Depends(oauth2_scheme),
        auth_use_case: AuthUseCase = Depends(get_auth_use_case),
    ) -> AuthUser:
        user = await auth_use_case.get_current_user(token=token)
        if required_permission not in user.permissions:
            raise PermissionDeniedException(
                f"Missing required permission: {required_permission}"
            )
        return user

    return get_current_active_user
