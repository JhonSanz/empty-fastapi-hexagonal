from typing import Optional

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.database_connection import Base


class SMTPConfigORM(Base):
    """
    SQLAlchemy ORM model for the SMTP configuration.

    NOTE: `password` is stored in plaintext. If this ever leaves a toy/dev
    project, encrypt it at rest (e.g. via a KMS-backed field or a secrets
    manager) instead of a raw column.
    """

    __tablename__ = "Smtp"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    server: Mapped[str] = mapped_column(String(300))
    port: Mapped[str] = mapped_column(String(300))
    user: Mapped[str] = mapped_column(String(300))
    password: Mapped[str] = mapped_column(String(300))
    receivers: Mapped[Optional[list]] = mapped_column(JSON, default=list)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
