from bcrypt import gensalt, hashpw

from src.user.domain.repository import UserRepository
from src.user.domain.entities import User, CreateUserData
from src.user.domain.unit_of_work import UnitOfWork
from src.user.domain.exceptions import UserAlreadyExistException
from src.user.domain.password_policy import validate_password_strength


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
        validate_password_strength(data.password)
        await self._check_email_unique(data.email)

        data.password = self._hash_password(data.password)
        user = await self.user_repository.create(data=data)

        if self.roles:
            await self.user_repository.check_roles_exist(roles=self.roles)
            await self.user_repository.bulk_link_roles_to_user(
                user_id=user.id, roles_ids=self.roles
            )

        await self.unit_of_work.commit()
        return user

    async def _check_email_unique(self, email: str) -> None:
        existing = await self.user_repository.get_by_email(email=email)
        if existing:
            raise UserAlreadyExistException(
                f"User with email {email} already exists"
            )

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
