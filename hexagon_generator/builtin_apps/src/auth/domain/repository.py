from abc import ABC, abstractmethod

from src.auth.application.schemas import AuthUser


class AuthRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> AuthUser | None: ...
