from src.smtp.domain.entities import SMTPConfig, UpdateSMTPConfigData
from src.smtp.domain.repository import SMTPRepository
from src.smtp.domain.unit_of_work import UnitOfWork


class UpdateUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        smtp_repository: SMTPRepository,
    ):
        self.unit_of_work = unit_of_work
        self.smtp_repository = smtp_repository

    async def execute(self, *, smtp_id: int, data: UpdateSMTPConfigData) -> SMTPConfig:
        smtp_config = await self.smtp_repository.update(id=smtp_id, data=data)
        await self.unit_of_work.commit()
        return smtp_config
