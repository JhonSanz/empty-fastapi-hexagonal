DOMAIN_MODELS_TEMPLATE = """
from sqlalchemy import (
    Integer,
    PrimaryKeyConstraint,
    Text,
)
from sqlalchemy.orm import mapped_column
from src.common.database_connection import Base


class {{ model_pascal_case }}(Base):
    # TODO:
    __tablename__ = "{{ model_pascal_case }}"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="{{ model_pascal_case }}_pkey"),
    )

    id = mapped_column(Integer)
    # name = mapped_column(Text, nullable=False)
"""
