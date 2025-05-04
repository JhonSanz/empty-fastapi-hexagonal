from sqlalchemy.orm import Session

from src.user.application.interfaces import UserServiceInterface
from src.user.application.schemas import UpdateUserRequest
from src.user.domain.exceptions import UserNotFoundException
from src.user.domain.models import User
from src.user.domain.repository import UserRepository


class UpdateUseCase:
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

    async def execute(self, *, user_id: int, user_request: UpdateUserRequest) -> None:
        if user_request.is_empty():
            return
        if user_request.model_dump(exclude_none=True, exclude={"roles"}):
            await self.user_repository.update(id=user_id, data=user_request)
        await self.user_service.check_and_link_roles(
            roles=user_request.roles, user_id=user_id
        )
        self.database.commit()
        return
