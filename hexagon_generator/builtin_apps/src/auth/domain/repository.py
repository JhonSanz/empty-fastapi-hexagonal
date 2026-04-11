from abc import ABC, abstractmethod

from src.auth.application.schemas import User


class AuthRepository(ABC):
    @abstractmethod
    def get_user_by_identification(self, identification: str) -> User | None: ...
