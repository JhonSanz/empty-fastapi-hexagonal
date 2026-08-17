from src.smtp.domain.entities import SMTPConfig
from src.smtp.domain.repository import SMTPRepository
from src.smtp.domain.unit_of_work import UnitOfWork
from src.smtp.application.schemas import FilterParams


class ListUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        smtp_repository: SMTPRepository,
    ):
        self.unit_of_work = unit_of_work
        self.smtp_repository = smtp_repository

    async def execute(self, *, filter_params: FilterParams) -> tuple[list[SMTPConfig], int]:
        return await self.smtp_repository.get(
            skip=filter_params.skip,
            limit=filter_params.limit,
        )
