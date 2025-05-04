from sqlalchemy.orm import Session

from src.auth.application.service import AuthService
from src.user.application.interfaces import UserServiceInterface
from src.user.application.schemas import FilterParams, UpdateUserRequest
from src.user.domain.models import User
from src.user.domain.repository import UserRepository


class ChangePasswordUseCase:
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

    async def execute(self, *, user_id: str, password: str) -> User:
        data = self.auth_service.decode_access_token(token=user_id)
        user_id = data["user"]
        filter_params = FilterParams()
        user_found = await self.user_repository.get_by_id(
            id=user_id, filter_params=filter_params
        )

        new_password = self.user_service.hash_password(password=password)
        user_data = UpdateUserRequest(password=new_password)
        await self.user_repository.update(id=user_found.id, data=user_data)

        self.database.commit()
        return user_found
