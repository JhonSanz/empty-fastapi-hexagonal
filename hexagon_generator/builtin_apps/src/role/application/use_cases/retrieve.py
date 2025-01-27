from src.role.domain.repository import RoleRepository
from src.role.domain.exceptions import RoleNotFoundException
from src.role.domain.models import Role
from src.role.application.interfaces import RoleServiceInterface
from src.role.application.schemas import FilterParams
from sqlalchemy.orm import Session


class RetrieveUseCase:
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

    async def execute(self, *, role_id: int, filter_params: FilterParams) -> Role:
        data = await self.role_repository.get_by_id(
            id=role_id, filter_params=filter_params
        )
        return data
