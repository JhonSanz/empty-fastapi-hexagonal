from abc import ABC, abstractmethod

from src.smtp.application.schemas import SMTPBase


class SMTPServiceInterface(ABC):
    @abstractmethod
    def my_method(self, my_param: None) -> None: ...


class SMTPProviderInterface(ABC):

    @abstractmethod
    async def auth(self) -> None: ...

    @abstractmethod
    async def send(
        self, *, recipient: str, sender: str, subject: str, message: str
    ) -> None: ...

    @abstractmethod
    async def get_smtp_credentials(self) -> SMTPBase: ...
