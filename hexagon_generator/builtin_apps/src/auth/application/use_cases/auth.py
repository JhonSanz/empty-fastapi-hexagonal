from sqlalchemy.orm import Session
from src.auth.application.schemas import User
from src.auth.domain.repository import AuthRepository
from src.auth.application.service import AuthService
import jwt
from src.auth.domain.exceptions import InvalidTokenException, UserNotFoundException


class AuthUseCase:
    def __init__(
        self, *, database: Session, auth_repo: AuthRepository, auth_service: AuthService
    ):
        self.database = database
        self.auth_repo = auth_repo
        self.auth_service = auth_service

    async def authenticate_user(self, *, identification: str, password: str) -> str:
        user = self.auth_repo.get_user_by_identification(self.database, identification)
        if not user or not self.auth_service.verify_password(password, user.password):
            raise InvalidTokenException()
        token = self.auth_service.create_access_token(data={"sub": user.identification})
        return token

    async def get_current_user(self, *, token: str) -> User:
        try:
            payload = self.auth_service.decode_access_token(token)
            identification = payload.get("sub")
            if not identification:
                raise InvalidTokenException()
            user = self.auth_repo.get_user_by_identification(self.database, identification)
            if not user:
                raise UserNotFoundException()
            return user
        except jwt.PyJWTError:
            raise InvalidTokenException()