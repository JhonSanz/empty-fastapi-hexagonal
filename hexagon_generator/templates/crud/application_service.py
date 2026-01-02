APPLICATION_SERVICE_TEMPLATE = """
from src.{{ model_snake_case }}.application.interfaces import {{ model_pascal_case }}ServiceInterface
from src.{{ model_snake_case }}.domain.repository import {{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.domain.models import {{ model_pascal_case }}
from src.{{ model_snake_case }}.domain.dtos import (
    Create{{ model_pascal_case }}DTO,
    Update{{ model_pascal_case }}DTO,
    {{ model_pascal_case }}FilterDTO,
)


class {{ model_pascal_case }}Service({{ model_pascal_case }}ServiceInterface):
    \"""
    Application service for {{ model_pascal_case }} business logic.

    This service acts as the public API for the {{ model_snake_case }} module,
    orchestrating operations and enforcing business rules.
    \"""

    def __init__(self, repository: {{ model_pascal_case }}Repository):
        self._repository = repository

    async def get_by_id(self, *, id: int) -> {{ model_pascal_case }}:
        \"""
        Get a {{ model_pascal_case }} by its ID.

        Args:
            id: ID of the {{ model_pascal_case }}

        Returns:
            {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"""
        # TODO: Add business logic validations if needed
        return await self._repository.get_by_id(id=id)

    async def get(self, *, filter_dto: {{ model_pascal_case }}FilterDTO) -> tuple[list[{{ model_pascal_case }}], int]:
        \"""
        Get a list of {{ model_pascal_case }}s with filtering and pagination.

        Args:
            filter_dto: Filtering and pagination parameters

        Returns:
            Tuple of (list of {{ model_pascal_case }}s, total count)
        \"""
        # TODO: Add business logic validations if needed
        return await self._repository.get(filter_dto=filter_dto)

    async def create(self, *, data: Create{{ model_pascal_case }}DTO) -> {{ model_pascal_case }}:
        \"""
        Create a new {{ model_pascal_case }}.

        Args:
            data: Data for creating the {{ model_pascal_case }}

        Returns:
            Created {{ model_pascal_case }} instance
        \"""
        # TODO: Add business logic validations if needed
        return await self._repository.create(data=data)

    async def update(self, *, id: int, data: Update{{ model_pascal_case }}DTO) -> {{ model_pascal_case }}:
        \"""
        Update an existing {{ model_pascal_case }}.

        Args:
            id: ID of the {{ model_pascal_case }} to update
            data: New data for the {{ model_pascal_case }}

        Returns:
            Updated {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"""
        # TODO: Add business logic validations if needed
        return await self._repository.update(id=id, data=data)

    async def delete(self, *, id: int) -> {{ model_pascal_case }}:
        \"""
        Delete a {{ model_pascal_case }}.

        Args:
            id: ID of the {{ model_pascal_case }} to delete

        Returns:
            Deleted {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"""
        # TODO: Add business logic validations if needed
        return await self._repository.delete(id=id)

    # TODO: Add additional business logic methods here
"""
