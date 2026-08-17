from src.smtp.domain.entities import SMTPConfig, CreateSMTPConfigData
from src.smtp.domain.repository import SMTPRepository
from src.smtp.domain.unit_of_work import UnitOfWork


class CreateUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        smtp_repository: SMTPRepository,
    ):
        self.unit_of_work = unit_of_work
        self.smtp_repository = smtp_repository

    async def execute(self, *, data: CreateSMTPConfigData) -> SMTPConfig:
        smtp_config = await self.smtp_repository.create(data=data)
        await self.unit_of_work.commit()
        return smtp_config
