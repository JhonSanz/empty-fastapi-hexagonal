from src.smtp.domain.repository import SMTPRepository
from src.smtp.domain.exceptions import SMTPNotFoundException
from src.smtp.domain.models import SMTP
from src.smtp.application.interfaces import SMTPServiceInterface

from sqlalchemy.orm import Session

from src.smtp.application.schemas import FilterParams


class ListUseCase:
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

    async def execute(self, *, filter_params: FilterParams) -> tuple[list[SMTP], int]:
        # TODO: your logic here
        data, count = await self.smtp_repository.get(filter_params=filter_params)
        return data, count
