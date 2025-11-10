DOMAIN_REPOSITORY_TEMPLATE = """
from abc import ABC, abstractmethod

from src.{{ model_snake_case }}.domain.models import {{ model_pascal_case }}
from src.{{ model_snake_case }}.application.schemas import (
    Create{{ model_pascal_case }}Request,
    Update{{ model_pascal_case }}Request,
    FilterParams,
)


class {{ model_pascal_case }}Repository(ABC):
    \"\"\"
    Abstract repository for {{ model_pascal_case }} operations.

    Defines the contract for {{ model_pascal_case }} data access operations.
    Implementations should handle all database-specific logic.
    \"\"\"

    @abstractmethod
    async def get_by_id(self, *, id: int) -> {{ model_pascal_case }}:
        \"\"\"
        Get a {{ model_pascal_case }} by its ID.

        Args:
            id: ID of the {{ model_pascal_case }}

        Returns:
            {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"\"\"
        ...

    @abstractmethod
    async def get(self, *, filter_params: FilterParams) -> tuple[list[{{ model_pascal_case }}], int]:
        \"\"\"
        Get a list of {{ model_pascal_case }}s with filtering and pagination.

        Args:
            filter_params: Filtering and pagination parameters

        Returns:
            Tuple of (list of {{ model_pascal_case }}s, total count)
        \"\"\"
        ...

    @abstractmethod
    async def create(self, *, data: Create{{ model_pascal_case }}Request) -> {{ model_pascal_case }}:
        \"\"\"
        Create a new {{ model_pascal_case }}.

        Args:
            data: Data for creating the {{ model_pascal_case }}

        Returns:
            Created {{ model_pascal_case }} instance
        \"\"\"
        ...

    @abstractmethod
    async def update(self, *, id: int, data: Update{{ model_pascal_case }}Request) -> {{ model_pascal_case }}:
        \"\"\"
        Update an existing {{ model_pascal_case }}.

        Args:
            id: ID of the {{ model_pascal_case }} to update
            data: New data for the {{ model_pascal_case }}

        Returns:
            Updated {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"\"\"
        ...

    @abstractmethod
    async def delete(self, *, id: int) -> {{ model_pascal_case }}:
        \"\"\"
        Delete a {{ model_pascal_case }}.

        Args:
            id: ID of the {{ model_pascal_case }} to delete

        Returns:
            Deleted {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"\"\"
        ...
"""