from abc import ABC, abstractmethod


class AuthServiceInterface(ABC):
    @abstractmethod
    def generate_token(self, user_id: int) -> str:
        pass
