import os
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from src.auth.application.service import AuthService
from src.auth.dependencies.get_user_with_permissions import get_user_with_permission
from src.common.database_connection import get_db
from src.common.std_response import StandardResponse, std_response
from src.config import settings
from src.role.infrastructure.database import ORMRoleRepository
from src.smtp.dependencies.send_email import send_email
from src.user.application.handlers import (
    change_password_handler,
    create_handler,
    delete_handler,
    forgot_password_handler,
    list_handler,
    retrieve_handler,
    update_handler,
)
from src.user.application.schemas import (
    CreateUserRequest,
    FilterParams,
    ImportUsers,
    UpdateUserRequest,
    UserInDBBase,
)
from src.user.application.service import UserService
from src.user.application.use_cases import (
    CreateUseCase,
    DeleteUseCase,
    ListUseCase,
    RetrieveUseCase,
    UpdateUseCase,
)
from src.user.application.use_cases.change_password import ChangePasswordUseCase
from src.user.application.use_cases.forgot_password import PasswordUseCase
from src.user.domain.models import User
from src.user.infrastructure.database import ORMUserRepository

router = APIRouter()


@router.post("/create", response_model=StandardResponse[UserInDBBase])
async def create_endpoint(
    create_user_request: CreateUserRequest,
    background_tasks: BackgroundTasks,
    database: Session = Depends(get_db),
    # _=Depends(get_user_with_permission("user.create")),
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

    task_args = {
        "db": database,
        "email": result.email,
        "subject": "Bienvenido a la plataforma",
        "message": "Bienvenido a la plataforma",
    }
    background_tasks.add_task(send_email, **task_args)

    return std_response(data=result)


@router.get("/list", response_model=StandardResponse[list[UserInDBBase]])
async def list_endpoint(
    filter_params: Annotated[FilterParams, Query()],
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("user.list")),
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
    _=Depends(get_user_with_permission("user.get")),
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
    _=Depends(get_user_with_permission("user.update")),
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
async def delete_endpoint(
    user_id: int,
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("user.delete")),
):
    user_repo = ORMUserRepository(db=database)
    user_service = UserService(user_repository=user_repo)
    delete_use_case = DeleteUseCase(
        database=database, user_repository=user_repo, user_service=user_service
    )
    result = await delete_handler(user_id=user_id, delete_use_case=delete_use_case)
    return std_response(data=result)


# @router.post("/import-users", response_model=StandardResponse[UserInDBBase])
# async def upload_excel(
#     file: UploadFile = File(...), database: Session = Depends(get_db)
# ):
#     if not file.filename.endswith((".csv", ".xlsx")):
#         raise HTTPException(
#             status_code=400, detail="El archivo debe ser de tipo Excel (.csv o .xlsx)"
#         )
#     await import_data(
#         db=database,
#         SQLAlchemyModel=User,
#         pydantic_validator=(ImportUsers, "users"),
#         uploaded_file=file,
#     )
#     return std_response()


@router.post("/forgot-password", response_model=StandardResponse[UserInDBBase])
async def forgot_password_endpoint(
    email: str,
    # background_tasks: BackgroundTasks,
    database: Session = Depends(get_db),
):
    auth_service = AuthService(
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
        access_token_expire_minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
    )
    user_repo = ORMUserRepository(db=database)
    user_service = UserService(user_repository=user_repo)
    password_use_case = PasswordUseCase(
        database=database,
        user_repository=user_repo,
        user_service=user_service,
        auth_service=auth_service,
    )
    token = await forgot_password_handler(
        email=email, password_use_case=password_use_case
    )
    msg = f"""
        <a href='{settings.frontend_url}/cambiar-contraseña?token={token}' target='__blank'>
            <h1>Haz click aqui para cambiar tu contraseña</h1>
        </a>
    """
    task_args = {
        "db": database,
        "email": email,
        "subject": "Cambio de contraseña",
        "message": msg,
    }
    was_sent, msg = await send_email(**task_args)
    if not was_sent:
        return std_response(status_code=status.HTTP_400_BAD_REQUEST, ok=False, msg=msg)

    database.commit()
    return std_response()


@router.post("/change-password", response_model=StandardResponse[UserInDBBase])
async def change_password_endpoint(
    token: str,
    password: str,
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("user.update")),
):
    auth_service = AuthService(
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
        access_token_expire_minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
    )
    user_repo = ORMUserRepository(db=database)
    user_service = UserService(user_repository=user_repo)
    password_use_case = ChangePasswordUseCase(
        database=database,
        user_repository=user_repo,
        user_service=user_service,
        auth_service=auth_service,
    )
    new_password = await change_password_handler(
        user_id=token, password=password, change_password_use_case=password_use_case
    )
    return std_response()
