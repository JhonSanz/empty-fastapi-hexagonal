from src.smtp.domain.entities import SMTPConfig
from src.smtp.domain.repository import SMTPRepository
from src.smtp.domain.unit_of_work import UnitOfWork


class DeleteUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        smtp_repository: SMTPRepository,
    ):
        self.unit_of_work = unit_of_work
        self.smtp_repository = smtp_repository

    async def execute(self, *, smtp_id: int) -> SMTPConfig:
        smtp_config = await self.smtp_repository.delete(id=smtp_id)
        await self.unit_of_work.commit()
        return smtp_config
