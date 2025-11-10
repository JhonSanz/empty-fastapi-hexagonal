APPLICATION_WEB_CASE_TEMPLATE_INIT = """
from .create import CreateUseCase
from .delete import DeleteUseCase
from .retrieve import RetrieveUseCase
from .list import ListUseCase
from .update import UpdateUseCase
"""

APPLICATION_WEB_CASE_TEMPLATE = """\"\"\"{{ action.capitalize() }} use case for {{ model_pascal_case }}.\"\"\"

from src.{{ model_snake_case }}.domain.repository import {{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.domain.models import {{ model_pascal_case }}
from src.{{ model_snake_case }}.domain.unit_of_work import UnitOfWork
from src.{{ model_snake_case }}.application.interfaces import {{ model_pascal_case }}ServiceInterface
from src.{{ model_snake_case }}.application.mappers import {{ model_pascal_case }}Mapper
{% if action in ["create", "update"] %}
from src.{{ model_snake_case }}.application.schemas import {{ action.capitalize() }}{{ model_pascal_case }}Request
{% endif %}
{% if action == "list" %}
from src.{{ model_snake_case }}.application.schemas import FilterParams
{% endif %}


class {{ action.capitalize() }}UseCase:
    \"\"\"
    Use case for {{ action }}ing a {{ model_pascal_case }}.

    This class encapsulates the business logic for {{ action }}ing a {{ model_pascal_case }}.
    \"\"\"

    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        {{ model_snake_case }}_repository: {{ model_pascal_case }}Repository,
        {{ model_snake_case }}_service: {{ model_pascal_case }}ServiceInterface
    ):
        \"\"\"
        Initialize the use case.

        Args:
            unit_of_work: Unit of Work for transaction management
            {{ model_snake_case }}_repository: Repository for {{ model_pascal_case }} data access
            {{ model_snake_case }}_service: Service for {{ model_pascal_case }} business logic
        \"\"\"
        self.unit_of_work = unit_of_work
        self.{{ model_snake_case }}_repository = {{ model_snake_case }}_repository
        self.{{ model_snake_case }}_service = {{ model_snake_case }}_service

    {% if action == "create" %}
    async def execute(self, *, {{ model_snake_case }}_request: {{ action.capitalize() }}{{ model_pascal_case }}Request) -> {{ model_pascal_case }}:
        \"\"\"
        Execute the create use case.

        Args:
            {{ model_snake_case }}_request: Data for creating the {{ model_pascal_case }}

        Returns:
            Created {{ model_pascal_case }} instance
        \"\"\"
        # Convert application schema to domain DTO
        create_dto = {{ model_pascal_case }}Mapper.to_create_dto({{ model_snake_case }}_request)

        # TODO: Add your business logic here (validation, transformations, etc.)

        # Create the {{ model_snake_case }}
        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.create(data=create_dto)

        # Commit the transaction
        self.unit_of_work.commit()

        return {{ model_snake_case }}

    {% elif action == "update" %}
    async def execute(self, *, {{ model_snake_case }}_id: int, {{ model_snake_case }}_request: {{ action.capitalize() }}{{ model_pascal_case }}Request) -> {{ model_pascal_case }}:
        \"\"\"
        Execute the update use case.

        Args:
            {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to update
            {{ model_snake_case }}_request: New data for the {{ model_pascal_case }}

        Returns:
            Updated {{ model_pascal_case }} instance
        \"\"\"
        # Convert application schema to domain DTO
        update_dto = {{ model_pascal_case }}Mapper.to_update_dto({{ model_snake_case }}_request)

        # TODO: Add your business logic here (validation, authorization, etc.)

        # Update the {{ model_snake_case }}
        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.update(
            id={{ model_snake_case }}_id,
            data=update_dto
        )

        # Commit the transaction
        self.unit_of_work.commit()

        return {{ model_snake_case }}

    {% elif action == "list" %}
    async def execute(self, *, filter_params: FilterParams) -> tuple[list[{{ model_pascal_case }}], int]:
        \"\"\"
        Execute the list use case.

        Args:
            filter_params: Filtering and pagination parameters

        Returns:
            Tuple of (list of {{ model_pascal_case }}s, total count)
        \"\"\"
        # Convert application schema to domain DTO
        filter_dto = {{ model_pascal_case }}Mapper.to_filter_dto(filter_params)

        # TODO: Add your business logic here (filtering, authorization, etc.)

        # Get the list of {{ model_snake_case }}s
        data, count = await self.{{ model_snake_case }}_repository.get(filter_dto=filter_dto)

        return data, count

    {% elif action == "retrieve" %}
    async def execute(self, *, {{ model_snake_case }}_id: int) -> {{ model_pascal_case }}:
        \"\"\"
        Execute the retrieve use case.

        Args:
            {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to retrieve

        Returns:
            Retrieved {{ model_pascal_case }} instance
        \"\"\"
        # TODO: Add your business logic here (authorization, data enrichment, etc.)

        # Get the {{ model_snake_case }}
        data = await self.{{ model_snake_case }}_repository.get_by_id(id={{ model_snake_case }}_id)

        return data

    {% elif action == "delete" %}
    async def execute(self, *, {{ model_snake_case }}_id: int) -> {{ model_pascal_case }}:
        \"\"\"
        Execute the delete use case.

        Args:
            {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to delete

        Returns:
            Deleted {{ model_pascal_case }} instance
        \"\"\"
        # TODO: Add your business logic here (authorization, cascading deletes, etc.)

        # Delete the {{ model_snake_case }}
        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.delete(id={{ model_snake_case }}_id)

        # Commit the transaction
        self.unit_of_work.commit()

        return {{ model_snake_case }}

    {% endif %}
"""
