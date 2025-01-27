from src.role.domain.repository import RoleRepository
from src.role.domain.exceptions import RoleNotFoundException
from src.role.domain.models import Role
from src.role.application.interfaces import RoleServiceInterface

from sqlalchemy.orm import Session


class DeleteUseCase:
    def __init__(
        self,
        *,
        database: Session,
        role_repository: RoleRepository,
        role_service: RoleServiceInterface
    ):
        self.database = database
        self.role_repository = role_repository
        self.role_service = role_service

    async def execute(self, *, role_id: int) -> None:
        await self.role_repository.delete(id=role_id)
        self.database.commit()
        return
