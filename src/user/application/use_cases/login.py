from src.user.domain.repository import UserRepository
from src.user.domain.exceptions import UserNotFoundException, InvalidPasswordException
from src.user.domain.models import User
from src.user.application.interfaces.login import AuthServiceInterface


class LoginUseCase:
    def __init__(
        self, *, user_repository: UserRepository, user_service: AuthServiceInterface
    ):
        self.user_repository = user_repository
        self.user_service = user_service

    def execute(self, username: str, password: str) -> str:
        user: User = self.user_repository.find_by_username(username)
        if not user:
            raise UserNotFoundException("User not found")
        if not user.verify_password(password):
            raise InvalidPasswordException("Invalid password")
        return self.user_service.generate_token(user.id)
