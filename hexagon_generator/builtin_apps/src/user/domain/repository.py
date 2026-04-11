from abc import ABC, abstractmethod

from src.user.domain.entities import (
    User,
    CreateUserData,
    UpdateUserData,
)


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int) -> User: ...

    @abstractmethod
    async def get(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        search: str | None = None,
        **filters,
    ) -> tuple[list[User], int]: ...

    @abstractmethod
    async def create(self, *, data: CreateUserData) -> User: ...

    @abstractmethod
    async def update(self, *, id: int, data: UpdateUserData) -> User: ...

    @abstractmethod
    async def delete(self, *, id: int) -> User: ...

    @abstractmethod
    async def get_by_email(self, *, email: str) -> User | None: ...

    @abstractmethod
    async def check_roles_exist(self, *, roles: list[int]) -> None: ...

    @abstractmethod
    async def bulk_link_roles_to_user(
        self, *, user_id: int, roles_ids: list[int]
    ) -> None: ...
