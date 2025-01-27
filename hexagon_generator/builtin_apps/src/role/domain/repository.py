from abc import ABC, abstractmethod
from src.role.domain.models import Role, Permission


class RoleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int, filter_params) -> Role: ...

    @abstractmethod
    async def get(self, *, id: int, filter_params) -> tuple[list[Role], int]: ...

    @abstractmethod
    async def create(self, *, data): ...

    @abstractmethod
    async def update(self, *, id: int, data): ...

    @abstractmethod
    async def delete(self, *, id: int): ...

    @abstractmethod
    async def get_permissions(self) -> tuple[list[Permission], int]: ...

    @abstractmethod
    async def check_permissions_exist(self, *, permissions: list[int]) -> None: ...

    @abstractmethod
    async def bulk_link_permissions_to_role(
        self, role_id: int, permission_ids: list[int]
    ) -> None: ...
