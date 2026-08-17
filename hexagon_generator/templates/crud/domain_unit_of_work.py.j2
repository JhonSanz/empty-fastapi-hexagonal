from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
