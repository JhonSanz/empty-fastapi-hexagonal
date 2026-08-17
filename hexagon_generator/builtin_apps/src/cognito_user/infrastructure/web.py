from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.cognito_auth.dependencies.get_user_with_permissions import get_user_with_permission
from src.common.database_connection import get_db
from src.common.std_response import StandardResponse, std_response
from src.cognito_user.domain.entities import UpdateUserData
from src.cognito_user.application.schemas import (
    FilterParams,
    UpdateUserRequest,
    UserResponse,
    UserListResponse,
)
from src.cognito_user.application.use_cases import (
    DeleteUseCase,
    ListUseCase,
    RetrieveUseCase,
    UpdateUseCase,
)
from src.cognito_user.infrastructure.database import ORMUserRepository
from src.cognito_user.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


# --- Dependencies ---


def get_repository(db: AsyncSession = Depends(get_db)) -> ORMUserRepository:
    return ORMUserRepository(db=db)


def get_unit_of_work(db: AsyncSession = Depends(get_db)) -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(session=db)


Repository = Annotated[ORMUserRepository, Depends(get_repository)]
UoW = Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)]
UserId = Annotated[int, Path(..., description="ID of the User", gt=0)]


@router.get(
    "",
    response_model=StandardResponse[list[UserListResponse]],
)
async def list_users(
    filter_params: Annotated[FilterParams, Query()],
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("user.list")),
):
    use_case = ListUseCase(unit_of_work=unit_of_work, user_repository=repository)
    result, count = await use_case.execute(filter_params=filter_params)
    return std_response(data=result, count=count)


@router.get(
    "/{user_id}",
    response_model=StandardResponse[UserResponse],
)
async def get_user(
    user_id: UserId,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("user.get")),
):
    use_case = RetrieveUseCase(unit_of_work=unit_of_work, user_repository=repository)
    result = await use_case.execute(user_id=user_id)
    return std_response(data=result)


@router.patch(
    "/{user_id}",
    response_model=StandardResponse[UserResponse],
)
async def update_user(
    user_id: UserId,
    user_data: UpdateUserRequest,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("user.update")),
):
    data = UpdateUserData(**user_data.model_dump(exclude={"roles"}, exclude_none=True))
    use_case = UpdateUseCase(
        unit_of_work=unit_of_work,
        user_repository=repository,
        roles=user_data.roles,
    )
    result = await use_case.execute(user_id=user_id, data=data)
    return std_response(data=result)


@router.delete(
    "/{user_id}",
    response_model=StandardResponse[UserResponse],
)
async def delete_user(
    user_id: UserId,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("user.delete")),
):
    use_case = DeleteUseCase(unit_of_work=unit_of_work, user_repository=repository)
    result = await use_case.execute(user_id=user_id)
    return std_response(data=result)
