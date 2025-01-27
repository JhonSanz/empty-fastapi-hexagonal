from src.role.domain.repository import RoleRepository
from src.role.domain.models import Role
from src.role.application.interfaces import RoleServiceInterface
from sqlalchemy.orm import Session
from src.role.application.schemas import FilterParams


class ListUseCase:
    def __init__(
        self,
        *,
        database: Session,
        role_repository: RoleRepository,
        role_service: RoleServiceInterface
    ):
        self.database = database
        self.role_repository = role_repository
        self.role_service = role_service

    async def execute(self, *, filter_params: FilterParams) -> tuple[list[Role], int]:
        data, count = await self.role_repository.get(filter_params=filter_params)
        return data, count
