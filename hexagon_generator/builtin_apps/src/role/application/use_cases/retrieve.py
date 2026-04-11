from src.role.domain.repository import RoleRepository
from src.role.domain.entities import Role
from src.role.domain.unit_of_work import UnitOfWork


class RetrieveUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        role_repository: RoleRepository,
    ):
        self.unit_of_work = unit_of_work
        self.role_repository = role_repository

    async def execute(self, *, role_id: int) -> Role:
        return await self.role_repository.get_by_id(id=role_id)
