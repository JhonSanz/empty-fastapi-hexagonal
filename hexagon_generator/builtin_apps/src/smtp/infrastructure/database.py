from dataclasses import fields

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.smtp.domain.entities import SMTPConfig, CreateSMTPConfigData, UpdateSMTPConfigData
from src.smtp.domain.exceptions import SMTPNotFoundException
from src.smtp.domain.repository import SMTPRepository
from src.smtp.infrastructure.models import SMTPConfigORM


class ORMSMTPRepository(SMTPRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    @staticmethod
    def _to_entity(orm_obj: SMTPConfigORM) -> SMTPConfig:
        return SMTPConfig(
            id=orm_obj.id,
            server=orm_obj.server,
            port=orm_obj.port,
            user=orm_obj.user,
            password=orm_obj.password,
            receivers=orm_obj.receivers or [],
        )

    async def get_by_id(self, *, id: int) -> SMTPConfig:
        stmt = select(SMTPConfigORM).where(SMTPConfigORM.id == id)
        result = await self.db.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if not orm_obj:
            raise SMTPNotFoundException(f"SMTP config with ID {id} not found")

        return self._to_entity(orm_obj)

    async def get(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[SMTPConfig], int]:
        count_stmt = select(func.count()).select_from(SMTPConfigORM)
        count_result = await self.db.execute(count_stmt)
        count = count_result.scalar()

        stmt = select(SMTPConfigORM).order_by(SMTPConfigORM.id.desc()).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        orm_objects = result.scalars().all()

        return [self._to_entity(obj) for obj in orm_objects], count

    async def create(self, *, data: CreateSMTPConfigData) -> SMTPConfig:
        data_dict = {f.name: getattr(data, f.name) for f in fields(data)}
        orm_obj = SMTPConfigORM(**data_dict)

        self.db.add(orm_obj)
        await self.db.flush()
        await self.db.refresh(orm_obj)

        return self._to_entity(orm_obj)

    async def update(self, *, id: int, data: UpdateSMTPConfigData) -> SMTPConfig:
        await self.get_by_id(id=id)

        update_data = {
            f.name: getattr(data, f.name)
            for f in fields(data)
            if getattr(data, f.name) is not None
        }

        if not update_data:
            return await self.get_by_id(id=id)

        stmt = update(SMTPConfigORM).where(SMTPConfigORM.id == id).values(**update_data)
        await self.db.execute(stmt)
        await self.db.flush()

        return await self.get_by_id(id=id)

    async def delete(self, *, id: int) -> SMTPConfig:
        entity = await self.get_by_id(id=id)

        stmt = delete(SMTPConfigORM).where(SMTPConfigORM.id == id)
        await self.db.execute(stmt)
        await self.db.flush()

        return entity
