from src.role.domain.repository import RoleRepository
from src.role.domain.entities import Role
from src.role.domain.unit_of_work import UnitOfWork
from src.role.application.schemas import FilterParams


class ListUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        role_repository: RoleRepository,
    ):
        self.unit_of_work = unit_of_work
        self.role_repository = role_repository

    async def execute(self, *, filter_params: FilterParams) -> tuple[list[Role], int]:
        return await self.role_repository.get(
            skip=filter_params.skip,
            limit=filter_params.limit,
            order_by=filter_params.order_by,
            search=filter_params.search,
            show_permissions=filter_params.show_permissions,
        )
