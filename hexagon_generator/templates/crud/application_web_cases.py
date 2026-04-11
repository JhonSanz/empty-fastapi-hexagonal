APPLICATION_WEB_CASE_TEMPLATE_INIT = """
from .create import CreateUseCase
from .delete import DeleteUseCase
from .retrieve import RetrieveUseCase
from .list import ListUseCase
from .update import UpdateUseCase
"""

APPLICATION_WEB_CASE_TEMPLATE = """\"\"\"{{ action.capitalize() }} use case for {{ model_pascal_case }}.\"\"\"

from src.{{ model_snake_case }}.domain.repository import {{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.domain.entities import {{ model_pascal_case }}
from src.{{ model_snake_case }}.domain.unit_of_work import UnitOfWork
{% if action == "create" %}
from src.{{ model_snake_case }}.domain.entities import Create{{ model_pascal_case }}Data
{% endif %}
{% if action == "update" %}
from src.{{ model_snake_case }}.domain.entities import Update{{ model_pascal_case }}Data
{% endif %}
{% if action == "list" %}
from src.{{ model_snake_case }}.application.schemas import FilterParams
{% endif %}


class {{ action.capitalize() }}UseCase:
    \"\"\"Use case for {{ action }}ing a {{ model_pascal_case }}.\"\"\"

    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        {{ model_snake_case }}_repository: {{ model_pascal_case }}Repository,
    ):
        self.unit_of_work = unit_of_work
        self.{{ model_snake_case }}_repository = {{ model_snake_case }}_repository

    {% if action == "create" %}
    async def execute(self, *, data: Create{{ model_pascal_case }}Data) -> {{ model_pascal_case }}:
        # TODO: Add your business logic here (validation, transformations, etc.)

        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.create(data=data)
        self.unit_of_work.commit()
        return {{ model_snake_case }}

    {% elif action == "update" %}
    async def execute(self, *, {{ model_snake_case }}_id: int, data: Update{{ model_pascal_case }}Data) -> {{ model_pascal_case }}:
        # TODO: Add your business logic here (validation, authorization, etc.)

        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.update(
            id={{ model_snake_case }}_id,
            data=data,
        )
        self.unit_of_work.commit()
        return {{ model_snake_case }}

    {% elif action == "list" %}
    async def execute(self, *, filter_params: FilterParams) -> tuple[list[{{ model_pascal_case }}], int]:
        # TODO: Add your business logic here (filtering, authorization, etc.)

        return await self.{{ model_snake_case }}_repository.get(
            skip=filter_params.skip,
            limit=filter_params.limit,
            order_by=filter_params.order_by,
            search=filter_params.search,
        )

    {% elif action == "retrieve" %}
    async def execute(self, *, {{ model_snake_case }}_id: int) -> {{ model_pascal_case }}:
        # TODO: Add your business logic here (authorization, data enrichment, etc.)

        return await self.{{ model_snake_case }}_repository.get_by_id(id={{ model_snake_case }}_id)

    {% elif action == "delete" %}
    async def execute(self, *, {{ model_snake_case }}_id: int) -> {{ model_pascal_case }}:
        # TODO: Add your business logic here (authorization, cascading deletes, etc.)

        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.delete(id={{ model_snake_case }}_id)
        self.unit_of_work.commit()
        return {{ model_snake_case }}

    {% endif %}
"""
