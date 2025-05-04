from sqlalchemy.orm import Session

from src.smtp.application.interfaces import SMTPServiceInterface
from src.smtp.application.schemas import UpdateSMTPRequest
from src.smtp.domain.exceptions import SMTPNotFoundException
from src.smtp.domain.models import SMTP
from src.smtp.domain.repository import SMTPRepository


class UpdateUseCase:
    def __init__(
        self,
        *,
        database: Session,
        smtp_repository: SMTPRepository,
        smtp_service: SMTPServiceInterface
    ):
        self.database = database
        self.smtp_repository = smtp_repository
        self.smtp_service = smtp_service

    async def execute(self, *, smtp_id: int, smtp_request: UpdateSMTPRequest) -> None:
        if smtp_request.is_empty():
            return
        await self.smtp_repository.update(id=smtp_id, data=smtp_request)
        self.database.commit()
        return
