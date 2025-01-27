from src.user.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase,
)
from src.user.application.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    FilterParams,
)
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
