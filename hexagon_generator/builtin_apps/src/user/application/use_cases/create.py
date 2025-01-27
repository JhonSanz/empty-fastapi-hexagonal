from src.user.domain.repository import UserRepository
from src.user.domain.exceptions import UserNotFoundException
from src.user.domain.models import User
from src.user.application.interfaces import UserServiceInterface
from src.user.application.schemas import CreateUserRequest

from sqlalchemy.orm import Session


class CreateUseCase:
    def __init__(
        self,
        *,
        database: Session,
        user_repository: UserRepository,
        user_service: UserServiceInterface
    ):
        self.database = database
        self.user_repository = user_repository
        self.user_service = user_service

    async def execute(self, *, user_request: CreateUserRequest) -> None:
        await self.user_service.user_can_be_created(user_request=user_request)
        user_request.password = self.user_service.hash_password(
            password=user_request.password
        )
        user_created = await self.user_repository.create(data=user_request)
        await self.user_service.check_and_link_roles(
            roles=user_request.roles, user_id=user_created.id
        )
        self.database.commit()
        return
