from abc import ABC, abstractmethod
from src.user.domain.models import User


class UserRepository(ABC):
    @abstractmethod
    async def find_by_username(self, username: str) -> User: ...

    @abstractmethod
    async def save(self, authentication: User): ...
