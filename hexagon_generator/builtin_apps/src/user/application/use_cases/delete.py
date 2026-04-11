from src.user.domain.repository import UserRepository
from src.user.domain.entities import User
from src.user.domain.unit_of_work import UnitOfWork


class DeleteUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository

    async def execute(self, *, user_id: int) -> User:
        user = await self.user_repository.delete(id=user_id)
        self.unit_of_work.commit()
        return user
