from src.user.domain.repository import UserRepository
from src.user.domain.entities import User
from src.user.domain.unit_of_work import UnitOfWork
from src.user.application.schemas import FilterParams


class ListUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository

    async def execute(self, *, filter_params: FilterParams) -> tuple[list[User], int]:
        return await self.user_repository.get(
            skip=filter_params.skip,
            limit=filter_params.limit,
            order_by=filter_params.order_by,
            search=filter_params.search,
            email=filter_params.email,
            name=filter_params.name,
            is_active=filter_params.is_active,
        )
