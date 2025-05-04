from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.auth.dependencies.get_user_with_permissions import get_user_with_permission
from src.common.database_connection import get_db
from src.common.std_response import StandardResponse, std_response
from src.smtp.application.handlers import (
    create_handler,
    delete_handler,
    list_handler,
    retrieve_handler,
    update_handler,
)
from src.smtp.application.schemas import (
    CreateSMTPRequest,
    FilterParams,
    SMTPInDBBase,
    UpdateSMTPRequest,
)
from src.smtp.application.service import SMTPService
from src.smtp.application.use_cases import (
    CreateUseCase,
    DeleteUseCase,
    ListUseCase,
    RetrieveUseCase,
    UpdateUseCase,
)
from src.smtp.dependencies.send_email import send_email
from src.smtp.infrastructure.database import ORMSMTPRepository

router = APIRouter()


@router.post("/create", response_model=StandardResponse[SMTPInDBBase])
async def create_endpoint(
    create_smtp_request: CreateSMTPRequest,
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("smtp.create")),
):
    smtp_repo = ORMSMTPRepository(db=database)
    smtp_service = SMTPService()
    create_use_case = CreateUseCase(
        database=database, smtp_repository=smtp_repo, smtp_service=smtp_service
    )
    result = await create_handler(
        create_smtp_request=create_smtp_request, create_use_case=create_use_case
    )
    return std_response(data=result)


@router.get("/list", response_model=StandardResponse[list[SMTPInDBBase]])
async def list_endpoint(
    filter_params: Annotated[FilterParams, Query()],
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("smtp.list")),
):
    smtp_repo = ORMSMTPRepository(db=database)
    smtp_service = SMTPService()
    list_use_case = ListUseCase(
        database=database, smtp_repository=smtp_repo, smtp_service=smtp_service
    )
    result, count = await list_handler(
        filter_params=filter_params, list_use_case=list_use_case
    )
    return std_response(data=result, count=count)


@router.get("/{smtp_id}/retrieve", response_model=StandardResponse[SMTPInDBBase])
async def retrieve_endpoint(
    smtp_id: int,
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("smtp.get")),
):
    smtp_repo = ORMSMTPRepository(db=database)
    smtp_service = SMTPService()
    retrieve_use_case = RetrieveUseCase(
        database=database, smtp_repository=smtp_repo, smtp_service=smtp_service
    )
    result = await retrieve_handler(
        smtp_id=smtp_id, retrieve_use_case=retrieve_use_case
    )
    return std_response(data=result)


@router.put("/{smtp_id}/update", response_model=StandardResponse[SMTPInDBBase])
async def update_endpoint(
    smtp_id: int,
    update_smtp_request: UpdateSMTPRequest,
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("smtp.update")),
):
    smtp_repo = ORMSMTPRepository(db=database)
    smtp_service = SMTPService()
    update_use_case = UpdateUseCase(
        database=database, smtp_repository=smtp_repo, smtp_service=smtp_service
    )
    result = await update_handler(
        smtp_id=smtp_id,
        update_smtp_request=update_smtp_request,
        update_use_case=update_use_case,
    )
    return std_response(data=result)


@router.delete("/{smtp_id}/delete", response_model=StandardResponse[SMTPInDBBase])
async def delete_endpoint(
    smtp_id: int,
    database: Session = Depends(get_db),
    _=Depends(get_user_with_permission("smtp.delete")),
):
    smtp_repo = ORMSMTPRepository(db=database)
    smtp_service = SMTPService()
    delete_use_case = DeleteUseCase(
        database=database, smtp_repository=smtp_repo, smtp_service=smtp_service
    )
    result = await delete_handler(smtp_id=smtp_id, delete_use_case=delete_use_case)
    return std_response(data=result)


@router.post("/test-email", response_model=StandardResponse)
async def test_email(
    database: Session = Depends(get_db),
):
    task_args = {
        "db": database,
        "subject": "Correo de prueba",
        "message": "Tu configuración SMTP funciona correctamente",
    }
    was_sent, msg = await send_email(**task_args)
    if not was_sent:
        return std_response(status_code=status.HTTP_400_BAD_REQUEST, ok=False, msg=msg)

    database.commit()
    return std_response()
