from src.user.domain.repository import UserRepository
from src.user.domain.entities import User, UpdateUserData
from src.user.domain.unit_of_work import UnitOfWork


class UpdateUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        roles: list[int] | None = None,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository
        self.roles = roles

    async def execute(self, *, user_id: int, data: UpdateUserData) -> User:
        user = await self.user_repository.update(id=user_id, data=data)

        if self.roles is not None:
            await self.user_repository.check_roles_exist(roles=self.roles)
            await self.user_repository.bulk_link_roles_to_user(
                user_id=user_id, roles_ids=self.roles
            )

        self.unit_of_work.commit()
        return user
