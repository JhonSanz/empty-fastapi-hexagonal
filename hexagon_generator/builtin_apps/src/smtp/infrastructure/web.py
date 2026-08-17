from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

# NOTE: if you generated `cognito_auth` instead of `auth`, change this import
# to `from src.cognito_auth.dependencies.get_user_with_permissions import
# get_user_with_permission` — both expose the same get_user_with_permission()
# shape, `smtp` itself doesn't care which auth flavor you picked.
from src.auth.dependencies.get_user_with_permissions import get_user_with_permission
from src.common.database_connection import get_db
from src.common.std_response import StandardResponse, std_response
from src.smtp.application.schemas import (
    CreateSMTPRequest,
    FilterParams,
    SMTPResponse,
    UpdateSMTPRequest,
)
from src.smtp.application.use_cases import (
    CreateUseCase,
    DeleteUseCase,
    ListUseCase,
    RetrieveUseCase,
    UpdateUseCase,
)
from src.smtp.dependencies.send_email import send_email
from src.smtp.domain.entities import CreateSMTPConfigData, UpdateSMTPConfigData
from src.smtp.infrastructure.database import ORMSMTPRepository
from src.smtp.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


router = APIRouter(
    prefix="/smtp",
    tags=["Smtp"],
)


# --- Dependencies ---


def get_repository(db: AsyncSession = Depends(get_db)) -> ORMSMTPRepository:
    return ORMSMTPRepository(db=db)


def get_unit_of_work(db: AsyncSession = Depends(get_db)) -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(session=db)


Repository = Annotated[ORMSMTPRepository, Depends(get_repository)]
UoW = Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)]
SMTPId = Annotated[int, Path(..., description="ID of the SMTP config", gt=0)]


@router.post(
    "",
    response_model=StandardResponse[SMTPResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_smtp(
    smtp_data: CreateSMTPRequest,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("smtp.create")),
):
    data = CreateSMTPConfigData(**smtp_data.model_dump())
    use_case = CreateUseCase(unit_of_work=unit_of_work, smtp_repository=repository)
    result = await use_case.execute(data=data)
    return std_response(data=result, status_code=status.HTTP_201_CREATED)


@router.get(
    "",
    response_model=StandardResponse[list[SMTPResponse]],
)
async def list_smtp(
    filter_params: Annotated[FilterParams, Query()],
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("smtp.list")),
):
    use_case = ListUseCase(unit_of_work=unit_of_work, smtp_repository=repository)
    result, count = await use_case.execute(filter_params=filter_params)
    return std_response(data=result, count=count)


@router.get(
    "/{smtp_id}",
    response_model=StandardResponse[SMTPResponse],
)
async def get_smtp(
    smtp_id: SMTPId,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("smtp.get")),
):
    use_case = RetrieveUseCase(unit_of_work=unit_of_work, smtp_repository=repository)
    result = await use_case.execute(smtp_id=smtp_id)
    return std_response(data=result)


@router.patch(
    "/{smtp_id}",
    response_model=StandardResponse[SMTPResponse],
)
async def update_smtp(
    smtp_id: SMTPId,
    smtp_data: UpdateSMTPRequest,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("smtp.update")),
):
    data = UpdateSMTPConfigData(**smtp_data.model_dump(exclude_none=True))
    use_case = UpdateUseCase(unit_of_work=unit_of_work, smtp_repository=repository)
    result = await use_case.execute(smtp_id=smtp_id, data=data)
    return std_response(data=result)


@router.delete(
    "/{smtp_id}",
    response_model=StandardResponse[SMTPResponse],
)
async def delete_smtp(
    smtp_id: SMTPId,
    repository: Repository,
    unit_of_work: UoW,
    _=Depends(get_user_with_permission("smtp.delete")),
):
    use_case = DeleteUseCase(unit_of_work=unit_of_work, smtp_repository=repository)
    result = await use_case.execute(smtp_id=smtp_id)
    return std_response(data=result)


@router.post(
    "/test-email",
    response_model=StandardResponse,
)
async def test_email(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_user_with_permission("smtp.update")),
):
    task_args = {
        "db": db,
        "subject": "Correo de prueba",
        "message": "Tu configuración SMTP funciona correctamente",
    }
    was_sent, msg = await send_email(**task_args)
    if not was_sent:
        return std_response(status_code=status.HTTP_400_BAD_REQUEST, ok=False, msg=msg)

    return std_response()
