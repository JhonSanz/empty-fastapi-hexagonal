from src.user.application.schemas import (
    CreateUserRequest,
    FilterParams,
    UpdateUserRequest,
)
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


async def create_handler(
    *, create_user_request: CreateUserRequest, create_use_case: CreateUseCase
):
    data = await create_use_case.execute(user_request=create_user_request)
    return data


async def list_handler(*, filter_params: FilterParams, list_use_case: ListUseCase):
    data, count = await list_use_case.execute(filter_params=filter_params)
    return data, count


async def retrieve_handler(
    *, user_id: int, filter_params: FilterParams, retrieve_use_case: RetrieveUseCase
):
    data = await retrieve_use_case.execute(user_id=user_id, filter_params=filter_params)
    return data


async def update_handler(
    *,
    user_id: int,
    update_user_request: UpdateUserRequest,
    update_use_case: UpdateUseCase
):
    data = await update_use_case.execute(
        user_id=user_id, user_request=update_user_request
    )
    return data


async def delete_handler(*, user_id: int, delete_use_case: DeleteUseCase):
    data = await delete_use_case.execute(user_id=user_id)
    return data


async def forgot_password_handler(
    *, email: str, password_use_case: PasswordUseCase
) -> str:
    new_password = await password_use_case.execute(email=email)
    return new_password


async def change_password_handler(
    *, user_id: int, password: str, change_password_use_case: ChangePasswordUseCase
) -> str:
    new_password = await change_password_use_case.execute(
        user_id=user_id, password=password
    )
    return new_password
