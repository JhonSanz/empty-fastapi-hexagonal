DOMAIN_UNIT_OF_WORK_TEMPLATE = """
\"\"\"
Unit of Work pattern for transaction management.

Defines the contract for managing database transactions
without exposing infrastructure details to the domain.
\"\"\"

from abc import ABC, abstractmethod
from typing import Any


class UnitOfWork(ABC):
    \"\"\"
    Abstract Unit of Work for managing transactions.

    Handles commit, rollback, and provides access to repositories.
    \"\"\"

    @abstractmethod
    def commit(self) -> None:
        \"\"\"Commit the current transaction.\"\"\"
        ...

    @abstractmethod
    def rollback(self) -> None:
        \"\"\"Rollback the current transaction.\"\"\"
        ...

    @abstractmethod
    def flush(self) -> None:
        \"\"\"Flush changes to the database without committing.\"\"\"
        ...

    def __enter__(self):
        \"\"\"Context manager entry.\"\"\"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        \"\"\"Context manager exit with automatic rollback on exception.\"\"\"
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
"""
