from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies.get_user_with_permissions import get_user_with_permission
from src.common.database_connection import get_db
from src.common.std_response import StandardResponse, std_response
from src.config import settings
from src.smtp.dependencies.send_email import send_email
from src.user.domain.entities import CreateUserData, UpdateUserData
from src.user.application.schemas import (
    CreateUserRequest,
    FilterParams,
    UpdateUserRequest,
    UserResponse,
    UserListResponse,
)
from src.user.application.use_cases import (
    CreateUseCase,
    DeleteUseCase,
    ListUseCase,
    RetrieveUseCase,
    UpdateUseCase,
)
from src.user.application.use_cases.change_password import ChangePasswordUseCase
from src.user.application.use_cases.forgot_password import ForgotPasswordUseCase
from src.user.infrastructure.database import ORMUserRepository
from src.user.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


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


@router.post(
    "/",
    response_model=StandardResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: CreateUserRequest,
    repository: Repository,
    unit_of_work: UoW,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    # _=Depends(get_user_with_permission("user.create")),
):
    data = CreateUserData(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        phone=user_data.phone,
        is_active=user_data.is_active,
    )
    use_case = CreateUseCase(
        unit_of_work=unit_of_work,
        user_repository=repository,
        roles=user_data.roles,
    )
    result = await use_case.execute(data=data)

    task_args = {
        "db": db,
        "email": result.email,
        "subject": "Bienvenido a la plataforma",
        "message": "Bienvenido a la plataforma",
    }
    background_tasks.add_task(send_email, **task_args)

    return std_response(data=result, status_code=status.HTTP_201_CREATED)


@router.get(
    "/",
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
    data = UpdateUserData(
        **user_data.model_dump(exclude={"roles"}, exclude_none=True)
    )
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


@router.post(
    "/forgot-password",
    response_model=StandardResponse,
)
async def forgot_password(
    email: str,
    repository: Repository,
    unit_of_work: UoW,
    db: AsyncSession = Depends(get_db),
):
    use_case = ForgotPasswordUseCase(
        unit_of_work=unit_of_work,
        user_repository=repository,
    )
    token = await use_case.execute(email=email)

    msg = f"""
        <a href='{settings.frontend_url}/cambiar-contraseña?token={token}' target='__blank'>
            <h1>Haz click aqui para cambiar tu contraseña</h1>
        </a>
    """
    task_args = {
        "db": db,
        "email": email,
        "subject": "Cambio de contraseña",
        "message": msg,
    }
    was_sent, msg = await send_email(**task_args)
    if not was_sent:
        return std_response(status_code=status.HTTP_400_BAD_REQUEST, ok=False, msg=msg)

    return std_response()


@router.post(
    "/change-password",
    response_model=StandardResponse,
)
async def change_password(
    token: str,
    password: str,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("user.update")),
):
    use_case = ChangePasswordUseCase(
        unit_of_work=unit_of_work,
        user_repository=repository,
    )
    await use_case.execute(token=token, password=password)
    return std_response()
