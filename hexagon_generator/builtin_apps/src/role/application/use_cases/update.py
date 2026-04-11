from src.role.domain.repository import RoleRepository
from src.role.domain.entities import Role, UpdateRoleData
from src.role.domain.unit_of_work import UnitOfWork


class UpdateUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        role_repository: RoleRepository,
        permissions: list[int] | None = None,
    ):
        self.unit_of_work = unit_of_work
        self.role_repository = role_repository
        self.permissions = permissions

    async def execute(self, *, role_id: int, data: UpdateRoleData) -> Role:
        role = await self.role_repository.update(id=role_id, data=data)

        if self.permissions is not None:
            await self.role_repository.check_permissions_exist(
                permissions=self.permissions
            )
            await self.role_repository.bulk_link_permissions_to_role(
                role_id=role_id, permission_ids=self.permissions
            )

        self.unit_of_work.commit()
        return role
