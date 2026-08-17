from abc import ABC, abstractmethod

from src.cognito_auth.application.schemas import CognitoUser


class AuthRepository(ABC):
    @abstractmethod
    async def get_user_by_cognito_sub(self, *, cognito_sub: str) -> CognitoUser | None: ...
