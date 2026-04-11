from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session

from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.infrastructure.database import ORMAuthRepository
from src.common.database_connection import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_auth_use_case(db: Session = Depends(get_db)) -> AuthUseCase:
    return AuthUseCase(auth_repo=ORMAuthRepository(db=db))


def get_user_with_permission(required_permission: str):
    async def get_current_active_user(
        token: str = Depends(oauth2_scheme),
        auth_use_case: AuthUseCase = Depends(get_auth_use_case),
    ):
        user = await auth_use_case.get_current_user(token=token)
        # permission_checker(permission=required_permission, user=user)
        return user

    return get_current_active_user
