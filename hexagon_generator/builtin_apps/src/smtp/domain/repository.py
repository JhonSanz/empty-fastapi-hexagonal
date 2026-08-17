from abc import ABC, abstractmethod

from src.smtp.domain.entities import SMTPConfig, CreateSMTPConfigData, UpdateSMTPConfigData


class SMTPRepository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int) -> SMTPConfig: ...

    @abstractmethod
    async def get(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[SMTPConfig], int]: ...

    @abstractmethod
    async def create(self, *, data: CreateSMTPConfigData) -> SMTPConfig: ...

    @abstractmethod
    async def update(self, *, id: int, data: UpdateSMTPConfigData) -> SMTPConfig: ...

    @abstractmethod
    async def delete(self, *, id: int) -> SMTPConfig: ...
