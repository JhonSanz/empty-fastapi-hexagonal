DOMAIN_REPOSITORY_TEMPLATE = """
from abc import ABC, abstractmethod

from src.{{ model_snake_case }}.domain.entities import (
    {{ model_pascal_case }},
    Create{{ model_pascal_case }}Data,
    Update{{ model_pascal_case }}Data,
)


class {{ model_pascal_case }}Repository(ABC):
    \"\"\"
    Abstract repository for {{ model_pascal_case }} operations.

    Defines the contract for {{ model_pascal_case }} data access.
    Implementations must convert between domain entities and their storage format.
    \"\"\"

    @abstractmethod
    async def get_by_id(self, *, id: int) -> {{ model_pascal_case }}:
        ...

    @abstractmethod
    async def get(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        search: str | None = None,
        **filters,
    ) -> tuple[list[{{ model_pascal_case }}], int]:
        ...

    @abstractmethod
    async def create(self, *, data: Create{{ model_pascal_case }}Data) -> {{ model_pascal_case }}:
        ...

    @abstractmethod
    async def update(self, *, id: int, data: Update{{ model_pascal_case }}Data) -> {{ model_pascal_case }}:
        ...

    @abstractmethod
    async def delete(self, *, id: int) -> {{ model_pascal_case }}:
        ...
"""
