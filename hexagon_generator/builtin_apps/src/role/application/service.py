from src.role.application.interfaces import RoleServiceInterface
from src.role.domain.repository import RoleRepository


class RoleService(RoleServiceInterface):
    def __init__(
        self,
        *,
        role_repository: RoleRepository,
    ):
        self.role_repository = role_repository

    async def check_and_link_permissions(
        self, *, role_id: int, permissions: list[int]
    ) -> None:
        if not permissions:
            return
        await self.role_repository.check_permissions_exist(permissions=permissions)
        await self.role_repository.bulk_link_permissions_to_role(
            role_id=role_id, permission_ids=permissions
        )
