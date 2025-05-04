import bcrypt
from sqlalchemy.orm import Session

from src.auth.application.service import AuthService
from src.config import settings
from src.user.application.interfaces import UserServiceInterface
from src.user.application.schemas import FilterParams, UpdateUserRequest
from src.user.domain.exceptions import UserNotFoundException
from src.user.domain.models import User
from src.user.domain.repository import UserRepository


class PasswordUseCase:
    def __init__(
        self,
        *,
        database: Session,
        user_repository: UserRepository,
        user_service: UserServiceInterface,
        auth_service: AuthService = None,
    ):
        self.database = database
        self.user_repository = user_repository
        self.user_service = user_service
        self.auth_service = auth_service

    async def execute(self, *, email: str) -> User:
        filter_params = FilterParams(email=email)
        data, count = await self.user_repository.get(filter_params=filter_params)
        user_found = data[0]
        if count == 0:
            raise UserNotFoundException(f"Usuario con correo {email} no existe")
        random_string = await self.user_service.generate_random_string(length=16)
        new_password = self.user_service.hash_password(password=random_string)
        user_data = UpdateUserRequest(password=new_password)
        await self.user_repository.update(id=user_found.id, data=user_data)

        data_to_encode = {"user": user_found.id, "new_password": new_password}
        token = self.auth_service.create_access_token(data=data_to_encode)
        return token
