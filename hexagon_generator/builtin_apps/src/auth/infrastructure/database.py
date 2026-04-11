from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.application.schemas import AuthUser
from src.auth.domain.repository import AuthRepository
from src.user.infrastructure.models import UserORM


class ORMAuthRepository(AuthRepository):
    def __init__(self, *, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> AuthUser | None:
        stmt = select(UserORM).where(UserORM.email == email)
        result = self.db.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if not orm_obj:
            return None

        return AuthUser(
            id=orm_obj.id,
            email=orm_obj.email,
            password=orm_obj.password,
        )
