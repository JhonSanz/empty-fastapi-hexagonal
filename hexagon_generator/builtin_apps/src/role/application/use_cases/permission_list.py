from src.role.domain.repository import RoleRepository
from src.role.domain.entities import Permission
from src.role.domain.unit_of_work import UnitOfWork


class ListPermissionUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        role_repository: RoleRepository,
    ):
        self.unit_of_work = unit_of_work
        self.role_repository = role_repository

    async def execute(self) -> tuple[list[Permission], int]:
        return await self.role_repository.get_permissions()
