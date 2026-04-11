INFRASTRUCTURE_MODELS_TEMPLATE = """
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, Text, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.common.database_connection import Base


class {{ model_pascal_case }}ORM(Base):
    \"\"\"
    SQLAlchemy ORM model for {{ model_pascal_case }}.

    This is the infrastructure representation. Domain logic should use
    the {{ model_pascal_case }} entity from domain/entities.py instead.
    \"\"\"

    __tablename__ = "{{ model_snake_case }}"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # TODO: Add your model columns here
    # Example:
    # name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<{{ model_pascal_case }}ORM(id={self.id})>"
"""
