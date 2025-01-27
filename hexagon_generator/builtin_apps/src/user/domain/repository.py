from abc import ABC, abstractmethod
from src.user.domain.models import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int, filter_params) -> User: ...

    @abstractmethod
    async def get(self, *, id: int, filter_params) -> tuple[list[User], int]: ...

    @abstractmethod
    async def create(self, *, data): ...

    @abstractmethod
    async def update(self, *, id: int, data): ...

    @abstractmethod
    async def delete(self, *, id: int): ...

    @abstractmethod
    async def check_roles_exist(self, *, roles): ...

    @abstractmethod
    async def bulk_link_roles_to_user(self, *, user_id, roles_ids): ...
