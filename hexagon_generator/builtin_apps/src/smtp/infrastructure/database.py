from src.smtp.application.schemas import (
    CreateSMTPRequest,
    FilterParams,
    SMTPInDBBase,
    UpdateSMTPRequest,
)
from src.smtp.domain.exceptions import SMTPNotFoundException
from src.smtp.domain.models import SMTP
from src.smtp.domain.repository import SMTPRepository


class ORMSMTPRepository(SMTPRepository):
    def __init__(self, *, db):
        self.db = db

    async def get_by_id(self, *, id: int) -> SMTP:
        existing_smtp = self.db.query(SMTP).filter(SMTP.id == id).first()
        if not existing_smtp:
            raise SMTPNotFoundException(f"SMTP con id {id} no encontrado")
        return existing_smtp

    async def get(self, *, filter_params: FilterParams) -> tuple[list[SMTP], int]:
        filters_ = {}
        smtp_query = self.db.query(SMTP).filter_by(**filters_).order_by(SMTP.id.desc())
        count = smtp_query.count()
        smtp = smtp_query.offset(filter_params.skip).limit(filter_params.limit).all()
        return smtp, count

    async def create(self, *, data: CreateSMTPRequest):
        data_ = data.model_dump()
        smtp_result = SMTP(**data_)
        self.db.add(smtp_result)
        self.db.flush()
        self.db.refresh(smtp_result)
        return smtp_result

    async def update(self, *, id: int, data: UpdateSMTPRequest):
        data_ = data.model_dump(exclude_none=True)
        smtp_result = (
            self.db.query(SMTP)
            .filter(SMTP.id == id)
            .update(data_, synchronize_session="fetch")
        )

        if smtp_result == 0:
            raise SMTPNotFoundException(f"SMTP con id {id} no encontrado")

        updated_smtp = self.db.query(SMTP).filter(SMTP.id == id).first()
        self.db.refresh(updated_smtp)
        return updated_smtp

    async def delete(self, *, id: int):
        existing_smtp = self.db.query(SMTP).filter(SMTP.id == id).first()
        if not existing_smtp:
            raise SMTPNotFoundException(f"SMTP con id {id} no encontrado")

        self.db.delete(existing_smtp)
        self.db.flush()
