from src.role.domain.repository import RoleRepository
from src.role.domain.entities import Role, CreateRoleData
from src.role.domain.unit_of_work import UnitOfWork


class CreateUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        role_repository: RoleRepository,
        permissions: list[int] | None = None,
    ):
        self.unit_of_work = unit_of_work
        self.role_repository = role_repository
        self.permissions = permissions or []

    async def execute(self, *, data: CreateRoleData) -> Role:
        role = await self.role_repository.create(data=data)

        if self.permissions:
            await self.role_repository.check_permissions_exist(
                permissions=self.permissions
            )
            await self.role_repository.bulk_link_permissions_to_role(
                role_id=role.id, permission_ids=self.permissions
            )

        await self.unit_of_work.commit()
        return role
