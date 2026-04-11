from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies.get_user_with_permissions import get_user_with_permission
from src.common.database_connection import get_db
from src.common.std_response import StandardResponse, std_response
from src.role.domain.entities import CreateRoleData, UpdateRoleData
from src.role.application.schemas import (
    CreateRoleRequest,
    FilterParams,
    UpdateRoleRequest,
    RoleResponse,
    RoleListResponse,
    PermissionResponse,
)
from src.role.application.use_cases import (
    CreateUseCase,
    DeleteUseCase,
    ListUseCase,
    RetrieveUseCase,
    UpdateUseCase,
    ListPermissionUseCase,
)
from src.role.infrastructure.database import ORMRoleRepository
from src.role.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


router = APIRouter(
    prefix="/role",
    tags=["Role"],
)


# --- Dependencies ---


def get_repository(db: AsyncSession = Depends(get_db)) -> ORMRoleRepository:
    return ORMRoleRepository(db=db)


def get_unit_of_work(db: AsyncSession = Depends(get_db)) -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(session=db)


Repository = Annotated[ORMRoleRepository, Depends(get_repository)]
UoW = Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)]
RoleId = Annotated[int, Path(..., description="ID of the Role", gt=0)]


@router.post(
    "/",
    response_model=StandardResponse[RoleResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    role_data: CreateRoleRequest,
    repository: Repository,
    unit_of_work: UoW,
    # _=Depends(get_user_with_permission("role.create")),
):
    data = CreateRoleData(name=role_data.name)
    use_case = CreateUseCase(
        unit_of_work=unit_of_work,
        role_repository=repository,
        permissions=role_data.permissions,
    )
    result = await use_case.execute(data=data)
    return std_response(data=result, status_code=status.HTTP_201_CREATED)


@router.get(
    "/",
    response_model=StandardResponse[list[RoleListResponse]],
)
async def list_roles(
    filter_params: Annotated[FilterParams, Query()],
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("role.list")),
):
    use_case = ListUseCase(unit_of_work=unit_of_work, role_repository=repository)
    result, count = await use_case.execute(filter_params=filter_params)
    return std_response(data=result, count=count)


@router.get(
    "/permissions",
    response_model=StandardResponse[list[PermissionResponse]],
)
async def list_permissions(
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("role.list")),
):
    use_case = ListPermissionUseCase(
        unit_of_work=unit_of_work, role_repository=repository
    )
    result, count = await use_case.execute()
    return std_response(data=result, count=count)


@router.get(
    "/{role_id}",
    response_model=StandardResponse[RoleResponse],
)
async def get_role(
    role_id: RoleId,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("role.get")),
):
    use_case = RetrieveUseCase(unit_of_work=unit_of_work, role_repository=repository)
    result = await use_case.execute(role_id=role_id)
    return std_response(data=result)


@router.patch(
    "/{role_id}",
    response_model=StandardResponse[RoleResponse],
)
async def update_role(
    role_id: RoleId,
    role_data: UpdateRoleRequest,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("role.update")),
):
    data = UpdateRoleData(name=role_data.name)
    use_case = UpdateUseCase(
        unit_of_work=unit_of_work,
        role_repository=repository,
        permissions=role_data.permissions,
    )
    result = await use_case.execute(role_id=role_id, data=data)
    return std_response(data=result)


@router.delete(
    "/{role_id}",
    response_model=StandardResponse[RoleResponse],
)
async def delete_role(
    role_id: RoleId,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("role.delete")),
):
    use_case = DeleteUseCase(unit_of_work=unit_of_work, role_repository=repository)
    result = await use_case.execute(role_id=role_id)
    return std_response(data=result)
