from src.smtp.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase,
)
from src.smtp.application.schemas import (
    CreateSMTPRequest,
    UpdateSMTPRequest,
    FilterParams,
)
from src.smtp.domain.models import SMTP


async def create_handler(
    *, create_smtp_request: CreateSMTPRequest, create_use_case: CreateUseCase
):
    data = await create_use_case.execute(smtp_request=create_smtp_request)
    return data


async def list_handler(*, filter_params: FilterParams, list_use_case: ListUseCase):
    data, count = await list_use_case.execute(filter_params=filter_params)
    return data, count


async def retrieve_handler(*, smtp_id: int, retrieve_use_case: RetrieveUseCase):
    data = await retrieve_use_case.execute(smtp_id=smtp_id)
    return data


async def update_handler(
    *,
    smtp_id: int,
    update_smtp_request: UpdateSMTPRequest,
    update_use_case: UpdateUseCase
):
    data = await update_use_case.execute(
        smtp_id=smtp_id, smtp_request=update_smtp_request
    )
    return data


async def delete_handler(*, smtp_id: int, delete_use_case: DeleteUseCase):
    data = await delete_use_case.execute(smtp_id=smtp_id)
    return data
