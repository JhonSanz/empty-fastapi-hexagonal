import os
from datetime import datetime, timedelta

import bcrypt
import jwt

from src.auth.application.schemas import AuthUser
from src.auth.domain.repository import AuthRepository
from src.auth.domain.exceptions import InvalidTokenException, UserNotFoundException


class AuthUseCase:
    def __init__(self, *, auth_repo: AuthRepository):
        self.auth_repo = auth_repo
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    async def authenticate_user(self, *, email: str, password: str) -> str:
        user = self.auth_repo.get_user_by_email(email)
        if not user or not self._verify_password(password, user.password):
            raise InvalidTokenException()
        return self._create_access_token(data={"sub": user.email})

    async def get_current_user(self, *, token: str) -> AuthUser:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            email = payload.get("sub")
            if not email:
                raise InvalidTokenException()
            user = self.auth_repo.get_user_by_email(email)
            if not user:
                raise UserNotFoundException()
            return user
        except jwt.PyJWTError:
            raise InvalidTokenException()

    def _create_access_token(self, *, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
