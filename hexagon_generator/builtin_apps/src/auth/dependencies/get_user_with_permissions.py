import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.infrastructure.database import UserRepository
from src.auth.application.service import AuthService
from src.common.database_connection import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_auth_use_case(database=Depends(get_db)) -> AuthUseCase:
    auth_repo = UserRepository()
    auth_service = AuthService(
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
        access_token_expire_minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
    )
    return AuthUseCase(
        database=database, auth_repo=auth_repo, auth_service=auth_service
    )


def get_user_with_permission(required_permission: str):
    async def get_current_active_user(
        token: str = Depends(oauth2_scheme),
        auth_use_case: AuthUseCase = Depends(get_auth_use_case),
    ):
        user = await auth_use_case.get_current_user(token=token)

        # permission_checker(database=database, permission=required_permission, user=user)
        return user

    return get_current_active_user
