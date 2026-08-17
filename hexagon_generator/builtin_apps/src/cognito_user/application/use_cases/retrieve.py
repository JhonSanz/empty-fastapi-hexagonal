from src.cognito_user.domain.repository import UserRepository
from src.cognito_user.domain.entities import User
from src.cognito_user.domain.unit_of_work import UnitOfWork


class RetrieveUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository

    async def execute(self, *, user_id: int) -> User:
        return await self.user_repository.get_by_id(id=user_id)
