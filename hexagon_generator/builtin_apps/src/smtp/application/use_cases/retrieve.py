from src.smtp.domain.entities import SMTPConfig
from src.smtp.domain.repository import SMTPRepository
from src.smtp.domain.unit_of_work import UnitOfWork


class RetrieveUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        smtp_repository: SMTPRepository,
    ):
        self.unit_of_work = unit_of_work
        self.smtp_repository = smtp_repository

    async def execute(self, *, smtp_id: int) -> SMTPConfig:
        return await self.smtp_repository.get_by_id(id=smtp_id)
