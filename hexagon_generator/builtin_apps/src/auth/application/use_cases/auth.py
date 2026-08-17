from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.auth.application.schemas import AuthUser
from src.auth.domain.repository import AuthRepository
from src.auth.domain.exceptions import InvalidTokenException, UserNotFoundException
from src.config import settings


class AuthUseCase:
    def __init__(self, *, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def authenticate_user(self, *, email: str, password: str) -> str:
        user = await self.auth_repo.get_user_by_email(email)
        if not user or not self._verify_password(password, user.password):
            raise InvalidTokenException()
        return self._create_access_token(data={"sub": user.email})

    async def get_current_user(self, *, token: str) -> AuthUser:
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            email = payload.get("sub")
            if not email:
                raise InvalidTokenException()
            user = await self.auth_repo.get_user_by_email(email)
            if not user:
                raise UserNotFoundException()
            return user
        except jwt.PyJWTError:
            raise InvalidTokenException()

    def _create_access_token(self, *, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
