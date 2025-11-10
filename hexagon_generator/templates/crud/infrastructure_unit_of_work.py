INFRASTRUCTURE_UNIT_OF_WORK_TEMPLATE = """
\"\"\"
SQLAlchemy implementation of Unit of Work pattern.
\"\"\"

from sqlalchemy.orm import Session

from src.{{ model_snake_case }}.domain.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    \"\"\"SQLAlchemy implementation of Unit of Work.\"\"\"

    def __init__(self, session: Session):
        \"\"\"
        Initialize the Unit of Work.

        Args:
            session: SQLAlchemy database session
        \"\"\"
        self.session = session

    def commit(self) -> None:
        \"\"\"Commit the current transaction.\"\"\"
        self.session.commit()

    def rollback(self) -> None:
        \"\"\"Rollback the current transaction.\"\"\"
        self.session.rollback()

    def flush(self) -> None:
        \"\"\"Flush changes to the database without committing.\"\"\"
        self.session.flush()
"""
