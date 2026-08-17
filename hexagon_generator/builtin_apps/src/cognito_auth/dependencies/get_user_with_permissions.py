from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.cognito_auth.application.schemas import CognitoUser
from src.cognito_auth.application.use_cases import CognitoAuthUseCase
from src.cognito_auth.domain.exceptions import PermissionDeniedException
from src.cognito_auth.infrastructure.database import ORMAuthRepository
from src.cognito_user.infrastructure.database import ORMUserRepository
from src.cognito_user.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.common.database_connection import get_db

# No password grant here: the frontend gets tokens straight from Cognito
# (Amplify / hosted UI) and just sends the ID token as a Bearer header.
bearer_scheme = HTTPBearer()


def get_auth_use_case(db: AsyncSession = Depends(get_db)) -> CognitoAuthUseCase:
    return CognitoAuthUseCase(
        auth_repo=ORMAuthRepository(db=db),
        user_repository=ORMUserRepository(db=db),
        unit_of_work=SQLAlchemyUnitOfWork(session=db),
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_use_case: CognitoAuthUseCase = Depends(get_auth_use_case),
) -> CognitoUser:
    """Resolve the caller's identity without requiring any specific permission."""
    return await auth_use_case.get_current_user(token=credentials.credentials)


def get_user_with_permission(required_permission: str):
    async def get_current_active_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        auth_use_case: CognitoAuthUseCase = Depends(get_auth_use_case),
    ) -> CognitoUser:
        user = await auth_use_case.get_current_user(token=credentials.credentials)
        if required_permission not in user.permissions:
            raise PermissionDeniedException(
                f"Missing required permission: {required_permission}"
            )
        return user

    return get_current_active_user
