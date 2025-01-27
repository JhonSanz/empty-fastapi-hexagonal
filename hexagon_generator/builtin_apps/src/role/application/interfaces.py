from abc import ABC, abstractmethod


class RoleServiceInterface(ABC):
    @abstractmethod
    async def check_and_link_permissions(
        self, role_id, permissions, role_repository
    ) -> None: ...
