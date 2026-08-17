from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.cognito_auth.application.schemas import CognitoUser
from src.cognito_auth.domain.repository import AuthRepository
from src.cognito_user.infrastructure.models import UserORM
from src.role.infrastructure.models import RoleORM


class ORMAuthRepository(AuthRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def get_user_by_cognito_sub(self, *, cognito_sub: str) -> CognitoUser | None:
        stmt = (
            select(UserORM)
            .where(UserORM.cognito_sub == cognito_sub)
            .options(selectinload(UserORM.roles).selectinload(RoleORM.permissions))
        )
        result = await self.db.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if not orm_obj:
            return None

        permissions = {
            permission.name
            for role in orm_obj.roles
            for permission in role.permissions
        }

        return CognitoUser(
            id=orm_obj.id,
            cognito_sub=orm_obj.cognito_sub,
            email=orm_obj.email,
            permissions=sorted(permissions),
        )
