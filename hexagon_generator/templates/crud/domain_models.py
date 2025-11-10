DOMAIN_MODELS_TEMPLATE = """
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, Text, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.common.database_connection import Base


class {{ model_pascal_case }}(Base):
    \"\"\"
    {{ model_pascal_case }} model.

    Represents a {{ model_pascal_case }} entity in the database.
    \"\"\"

    __tablename__ = "{{ model_snake_case }}"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # TODO: Add your model fields here
    # Example fields:
    # name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    # price: Mapped[float] = mapped_column(nullable=False)

    # Timestamp fields (automatically managed)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="Timestamp when the record was created"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp when the record was last updated"
    )

    def __repr__(self) -> str:
        \"\"\"String representation of the model.\"\"\"
        return f"<{{ model_pascal_case }}(id={self.id})>"
"""
