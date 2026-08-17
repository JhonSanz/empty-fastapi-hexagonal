from src.cognito_user.domain.repository import UserRepository
from src.cognito_user.domain.entities import User, CreateUserData
from src.cognito_user.domain.unit_of_work import UnitOfWork


class CreateUseCase:
    """
    Provisions the local shadow profile for a Cognito identity.

    Not exposed over the API directly — signup happens in Cognito, on the
    frontend. This is invoked by `cognito_auth`'s JIT-provisioning path the
    first time a valid token from a new `cognito_sub` shows up.
    """

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
        user = await self.user_repository.create(data=data)

        if self.roles:
            await self.user_repository.check_roles_exist(roles=self.roles)
            await self.user_repository.bulk_link_roles_to_user(
                user_id=user.id, roles_ids=self.roles
            )

        await self.unit_of_work.commit()
        return user
