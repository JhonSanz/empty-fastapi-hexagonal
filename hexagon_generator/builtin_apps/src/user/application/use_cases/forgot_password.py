from datetime import datetime, timedelta, timezone

import jwt

from src.user.domain.repository import UserRepository
from src.user.domain.unit_of_work import UnitOfWork
from src.user.domain.exceptions import UserNotFoundException
from src.config import settings

RESET_PASSWORD_PURPOSE = "password_reset"


class ForgotPasswordUseCase:
    """
    Issues a short-lived reset token for the given email.

    Does NOT touch the user's current password: the account stays usable
    until the user actually completes the flow via ChangePasswordUseCase.
    """

    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository

    async def execute(self, *, email: str) -> str:
        user = await self.user_repository.get_by_email(email=email)
        if not user:
            raise UserNotFoundException(f"User with email {email} does not exist")

        return self._create_token(user_id=user.id)

    @staticmethod
    def _create_token(*, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        payload = {"user": user_id, "purpose": RESET_PASSWORD_PURPOSE, "exp": expire}
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
