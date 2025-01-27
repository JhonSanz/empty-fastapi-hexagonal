from src.role.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase,
    ListPermissionUseCase,
)
from src.role.application.schemas import (
    CreateRoleRequest,
    UpdateRoleRequest,
    FilterParams,
)
from src.role.domain.models import Role


async def create_handler(
    *, create_role_request: CreateRoleRequest, create_use_case: CreateUseCase
):
    data = await create_use_case.execute(role_request=create_role_request)
    return data


async def list_handler(*, filter_params: FilterParams, list_use_case: ListUseCase):
    data, count = await list_use_case.execute(filter_params=filter_params)
    return data, count


async def retrieve_handler(
    *, role_id: int, filter_params: FilterParams, retrieve_use_case: RetrieveUseCase
):
    data = await retrieve_use_case.execute(role_id=role_id, filter_params=filter_params)
    return data


async def update_handler(
    *,
    role_id: int,
    update_role_request: UpdateRoleRequest,
    update_use_case: UpdateUseCase
):
    data = await update_use_case.execute(
        role_id=role_id, role_request=update_role_request
    )
    return data


async def delete_handler(*, role_id: int, delete_use_case: DeleteUseCase):
    data = await delete_use_case.execute(role_id=role_id)
    return data


async def list_permission_handler(*, list_permission_use_case: ListPermissionUseCase):
    data, count = await list_permission_use_case.execute()
    return data, count
