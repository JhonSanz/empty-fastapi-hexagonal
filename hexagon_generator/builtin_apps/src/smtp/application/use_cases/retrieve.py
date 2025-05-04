from src.smtp.domain.repository import SMTPRepository
from src.smtp.domain.exceptions import SMTPNotFoundException
from src.smtp.domain.models import SMTP
from src.smtp.application.interfaces import SMTPServiceInterface

from sqlalchemy.orm import Session


class RetrieveUseCase:
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

    async def execute(self, *, smtp_id: int) -> SMTP:
        # TODO: your logic here
        data = await self.smtp_repository.get_by_id(id=smtp_id)
        return data
