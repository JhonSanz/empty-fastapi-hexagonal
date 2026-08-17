import jwt
from bcrypt import gensalt, hashpw

from src.user.domain.repository import UserRepository
from src.user.domain.entities import UpdateUserData
from src.user.domain.unit_of_work import UnitOfWork
from src.user.domain.exceptions import InvalidResetTokenException
from src.user.domain.password_policy import validate_password_strength
from src.user.application.use_cases.forgot_password import RESET_PASSWORD_PURPOSE
from src.config import settings


class ChangePasswordUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository

    async def execute(self, *, token: str, password: str) -> None:
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
        except jwt.PyJWTError:
            raise InvalidResetTokenException("Invalid or expired reset token")

        if payload.get("purpose") != RESET_PASSWORD_PURPOSE:
            raise InvalidResetTokenException("Invalid or expired reset token")

        validate_password_strength(password)

        user_id = payload["user"]
        hashed_password = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
        await self.user_repository.update(
            id=user_id, data=UpdateUserData(password=hashed_password)
        )

        await self.unit_of_work.commit()
