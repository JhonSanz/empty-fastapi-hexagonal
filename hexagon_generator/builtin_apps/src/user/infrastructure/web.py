from fastapi import APIRouter, Depends, Query, status
from typing import Annotated
from src.common.std_response import std_response, StandardResponse
from src.common.database_connection import get_db
from sqlalchemy.orm import Session

from src.user.application.handlers import (
    create_handler,
    retrieve_handler,
    list_handler,
    update_handler,
    delete_handler,
)
from src.user.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase,
)
from src.user.application.schemas import (
    UserInDBBase,
    CreateUserRequest,
    UpdateUserRequest,
    FilterParams,
)
from src.user.infrastructure.database import ORMUserRepository
from src.user.application.service import UserService
from src.role.infrastructure.database import ORMRoleRepository


router = APIRouter()


@router.post("/create", response_model=StandardResponse[UserInDBBase])
async def create_endpoint(
    create_user_request: CreateUserRequest, database: Session = Depends(get_db)
):
    role_repo = ORMRoleRepository(db=database)
    user_repo = ORMUserRepository(db=database, role_repository=role_repo)
    user_service = UserService(user_repository=user_repo)
    create_use_case = CreateUseCase(
        database=database, user_repository=user_repo, user_service=user_service
    )
    result = await create_handler(
        create_user_request=create_user_request, create_use_case=create_use_case
    )
    return std_response(data=result)


@router.get("/list", response_model=StandardResponse[list[UserInDBBase]])
async def list_endpoint(
    filter_params: Annotated[FilterParams, Query()], database: Session = Depends(get_db)
):
    user_repo = ORMUserRepository(db=database)
    user_service = UserService(user_repository=user_repo)
    list_use_case = ListUseCase(
        database=database, user_repository=user_repo, user_service=user_service
    )
    result, count = await list_handler(
        filter_params=filter_params, list_use_case=list_use_case
    )
    return std_response(data=result, count=count)


@router.get("/{user_id}/retrieve", response_model=StandardResponse[UserInDBBase])
async def retrieve_endpoint(
    user_id: int,
    filter_params: Annotated[FilterParams, Query()],
    database: Session = Depends(get_db),
):
    user_repo = ORMUserRepository(db=database)
    user_service = UserService(user_repository=user_repo)
    retrieve_use_case = RetrieveUseCase(
        database=database, user_repository=user_repo, user_service=user_service
    )
    result = await retrieve_handler(
        filter_params=filter_params,
        user_id=user_id,
        retrieve_use_case=retrieve_use_case,
    )
    return std_response(data=result)


@router.put("/{user_id}/update", response_model=StandardResponse[UserInDBBase])
async def update_endpoint(
    user_id: int,
    update_user_request: UpdateUserRequest,
    database: Session = Depends(get_db),
):
    role_repo = ORMRoleRepository(db=database)
    user_repo = ORMUserRepository(db=database, role_repository=role_repo)
    user_service = UserService(user_repository=user_repo)
    update_use_case = UpdateUseCase(
        database=database, user_repository=user_repo, user_service=user_service
    )
    result = await update_handler(
        user_id=user_id,
        update_user_request=update_user_request,
        update_use_case=update_use_case,
    )
    return std_response(data=result)


@router.delete("/{user_id}/delete", response_model=StandardResponse[UserInDBBase])
async def delete_endpoint(user_id: int, database: Session = Depends(get_db)):
    user_repo = ORMUserRepository(db=database)
    user_service = UserService(user_repository=user_repo)
    delete_use_case = DeleteUseCase(
        database=database, user_repository=user_repo, user_service=user_service
    )
    result = await delete_handler(user_id=user_id, delete_use_case=delete_use_case)
    return std_response(data=result)
