from sqlalchemy.orm import Session

from src.role.application.interfaces import RoleServiceInterface
from src.role.application.schemas import UpdateRoleRequest
from src.role.domain.exceptions import RoleNotFoundException
from src.role.domain.models import Role
from src.role.domain.repository import RoleRepository


class UpdateUseCase:
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

    async def execute(self, *, role_id: int, role_request: UpdateRoleRequest) -> None:
        if role_request.is_empty():
            return
        if role_request.model_dump(exclude_none=True, exclude={"permissions"}):
            await self.role_repository.update(id=role_id, data=role_request)
        await self.role_service.check_and_link_permissions(
            role_id=role_id, permissions=role_request.permissions
        )
        self.database.commit()
        return
