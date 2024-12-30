DOMAIN_MODELS_TEMPLATE = """
# from sqlalchemy import (
#     Integer,
#     PrimaryKeyConstraint,
#     Text,
# )
# from sqlalchemy.orm import mapped_column
# from src.common.database_connection import Base

from src.common.database_connection import Base

# TODO: sqlalchemy models here

class {{ model_pascal_case }}(Base):
    # TODO:
    # __tablename__ = "Store"
    # __table_args__ = (
    #     PrimaryKeyConstraint("id", name="Store_pkey"),
    # )

    # id = mapped_column(Integer)
    # name = mapped_column(Text, nullable=False)
    pass
"""