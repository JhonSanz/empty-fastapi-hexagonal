from src.role.domain.repository import RoleRepository
from src.role.domain.models import Role
from src.role.application.interfaces import RoleServiceInterface
from sqlalchemy.orm import Session
from src.role.application.schemas import FilterParams


class ListPermissionUseCase:
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

    async def execute(self) -> tuple[list[Role], int]:
        data, count = await self.role_repository.get_permissions()
        return data, count
