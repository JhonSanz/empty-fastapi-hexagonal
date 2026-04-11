import re

from bcrypt import gensalt, hashpw

from src.user.domain.repository import UserRepository
from src.user.domain.entities import User, CreateUserData
from src.user.domain.unit_of_work import UnitOfWork
from src.user.domain.exceptions import UserAlreadyExistException, InvalidPasswordException


class CreateUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        roles: list[int] | None = None,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository
        self.roles = roles or []

    async def execute(self, *, data: CreateUserData) -> User:
        self._validate_password(data.password)
        await self._check_email_unique(data.email)

        data.password = self._hash_password(data.password)
        user = await self.user_repository.create(data=data)

        if self.roles:
            await self.user_repository.check_roles_exist(roles=self.roles)
            await self.user_repository.bulk_link_roles_to_user(
                user_id=user.id, roles_ids=self.roles
            )

        self.unit_of_work.commit()
        return user

    def _validate_password(self, password: str) -> None:
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if not re.match(pattern, password):
            raise InvalidPasswordException(
                "Password does not meet the required criteria"
            )

    async def _check_email_unique(self, email: str) -> None:
        existing = await self.user_repository.get_by_email(email=email)
        if existing:
            raise UserAlreadyExistException(
                f"User with email {email} already exists"
            )

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
