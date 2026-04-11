from abc import ABC, abstractmethod

from src.role.domain.entities import (
    Role,
    Permission,
    CreateRoleData,
    UpdateRoleData,
)


class RoleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int) -> Role: ...

    @abstractmethod
    async def get(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        search: str | None = None,
        show_permissions: bool = False,
        **filters,
    ) -> tuple[list[Role], int]: ...

    @abstractmethod
    async def create(self, *, data: CreateRoleData) -> Role: ...

    @abstractmethod
    async def update(self, *, id: int, data: UpdateRoleData) -> Role: ...

    @abstractmethod
    async def delete(self, *, id: int) -> Role: ...

    @abstractmethod
    async def get_permissions(self) -> tuple[list[Permission], int]: ...

    @abstractmethod
    async def check_permissions_exist(self, *, permissions: list[int]) -> None: ...

    @abstractmethod
    async def bulk_link_permissions_to_role(
        self, *, role_id: int, permission_ids: list[int]
    ) -> None: ...
