from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.auth.dependencies.get_user_with_permissions import get_user_with_permission
from src.common.database_connection import get_db
from src.common.std_response import StandardResponse, std_response
from src.role.application.handlers import (
    create_handler,
    delete_handler,
    list_handler,
    list_permission_handler,
    retrieve_handler,
    update_handler,
)
from src.role.application.schemas import (
    CreateRoleRequest,
    FilterParams,
    PermissionSchema,
    RoleInDBBase,
    UpdateRoleRequest,
)
from src.role.application.service import RoleService
from src.role.application.use_cases import (
    CreateUseCase,
    DeleteUseCase,
    ListPermissionUseCase,
    ListUseCase,
    RetrieveUseCase,
    UpdateUseCase,
)
from src.role.infrastructure.database import ORMRoleRepository

router = APIRouter()


@router.post("/create", response_model=StandardResponse[RoleInDBBase])
async def create_endpoint(
    create_role_request: CreateRoleRequest,
    database: Session = Depends(get_db),
    # _=Depends(get_user_with_permission("role.create")),
):
    role_repo = ORMRoleRepository(db=database)
    role_service = RoleService(role_repository=role_repo)
    create_use_case = CreateUseCase(
        database=database, role_repository=role_repo, role_service=role_service
    )
    result = await create_handler(
        create_role_request=create_role_request, create_use_case=create_use_case
    )
    return std_response(data=result)


@router.get("/list", response_model=StandardResponse[list[RoleInDBBase]])
async def list_endpoint(
    filter_params: Annotated[FilterParams, Query()],
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("role.list")),
):
    role_repo = ORMRoleRepository(db=database)
    role_service = RoleService(role_repository=role_repo)
    list_use_case = ListUseCase(
        database=database, role_repository=role_repo, role_service=role_service
    )
    result, count = await list_handler(
        filter_params=filter_params, list_use_case=list_use_case
    )
    return std_response(data=result, count=count)


@router.get("/{role_id}/retrieve", response_model=StandardResponse[RoleInDBBase])
async def retrieve_endpoint(
    role_id: int,
    filter_params: Annotated[FilterParams, Query()],
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("role.get")),
):
    role_repo = ORMRoleRepository(db=database)
    role_service = RoleService(role_repository=role_repo)
    retrieve_use_case = RetrieveUseCase(
        database=database, role_repository=role_repo, role_service=role_service
    )
    result = await retrieve_handler(
        role_id=role_id,
        retrieve_use_case=retrieve_use_case,
        filter_params=filter_params,
    )
    return std_response(data=result)


@router.put("/{role_id}/update", response_model=StandardResponse[RoleInDBBase])
async def update_endpoint(
    role_id: int,
    update_role_request: UpdateRoleRequest,
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("role.update")),
):
    role_repo = ORMRoleRepository(db=database)
    role_service = RoleService(role_repository=role_repo)
    update_use_case = UpdateUseCase(
        database=database, role_repository=role_repo, role_service=role_service
    )
    result = await update_handler(
        role_id=role_id,
        update_role_request=update_role_request,
        update_use_case=update_use_case,
    )
    return std_response(data=result)


@router.delete("/{role_id}/delete", response_model=StandardResponse[RoleInDBBase])
async def delete_endpoint(
    role_id: int,
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("role.delete")),
):
    role_repo = ORMRoleRepository(db=database)
    role_service = RoleService(role_repository=role_repo)
    delete_use_case = DeleteUseCase(
        database=database, role_repository=role_repo, role_service=role_service
    )
    result = await delete_handler(role_id=role_id, delete_use_case=delete_use_case)
    return std_response(data=result)


@router.get(
    "/permissions/list", response_model=StandardResponse[list[PermissionSchema]]
)
async def list_permissions_endpoint(
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("role.list")),
):
    role_repo = ORMRoleRepository(db=database)
    role_service = RoleService(role_repository=role_repo)
    list_permission_use_case = ListPermissionUseCase(
        database=database, role_repository=role_repo, role_service=role_service
    )
    result, count = await list_permission_handler(
        list_permission_use_case=list_permission_use_case
    )
    return std_response(data=result, count=count)
