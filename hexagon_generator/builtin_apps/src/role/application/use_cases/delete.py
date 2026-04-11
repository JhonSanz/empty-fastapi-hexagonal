from src.role.domain.repository import RoleRepository
from src.role.domain.entities import Role
from src.role.domain.unit_of_work import UnitOfWork


class DeleteUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        role_repository: RoleRepository,
    ):
        self.unit_of_work = unit_of_work
        self.role_repository = role_repository

    async def execute(self, *, role_id: int) -> Role:
        role = await self.role_repository.delete(id=role_id)
        await self.unit_of_work.commit()
        return role
