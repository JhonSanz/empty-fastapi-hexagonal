INFRASTRUCTURE_UNIT_OF_WORK_TEMPLATE = """
from sqlalchemy.ext.asyncio import AsyncSession

from src.{{ model_snake_case }}.domain.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def flush(self) -> None:
        await self.session.flush()
"""
