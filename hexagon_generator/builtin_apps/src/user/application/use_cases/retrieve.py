from src.user.domain.repository import UserRepository
from src.user.domain.exceptions import UserNotFoundException
from src.user.domain.models import User
from src.user.application.interfaces import UserServiceInterface
from sqlalchemy.orm import Session
from src.user.application.schemas import FilterParams


class RetrieveUseCase:
    def __init__(
        self,
        *,
        database: Session,
        user_repository: UserRepository,
        user_service: UserServiceInterface
    ):
        self.database = database
        self.user_repository = user_repository
        self.user_service = user_service

    async def execute(self, *, user_id: int, filter_params: FilterParams) -> User:
        data = await self.user_repository.get_by_id(
            id=user_id, filter_params=filter_params
        )
        return data
