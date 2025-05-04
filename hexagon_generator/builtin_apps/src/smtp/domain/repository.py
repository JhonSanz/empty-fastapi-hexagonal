from abc import ABC, abstractmethod
from src.smtp.domain.models import SMTP


class SMTPRepository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int) -> SMTP: ...

    @abstractmethod
    async def get(self, *, id: int, filter_params) -> tuple[list[SMTP], int]: ...

    @abstractmethod
    async def create(self, *, data): ...

    @abstractmethod
    async def update(self, *, id: int, data): ...

    @abstractmethod
    async def delete(self, *, id: int): ...
