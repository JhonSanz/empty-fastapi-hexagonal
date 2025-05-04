from sqlalchemy import JSON, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import mapped_column

from src.common.database_connection import Base


class SMTP(Base):
    __tablename__ = "Smtp"
    __table_args__ = (PrimaryKeyConstraint("id", name="Smtp_pkey"),)

    id = mapped_column(Integer)
    server = mapped_column(String(300))
    port = mapped_column(String(300))
    user = mapped_column(String(300))
    password = mapped_column(String(300))
    receivers = mapped_column(JSON, default=[])
