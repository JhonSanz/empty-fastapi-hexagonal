APPLICATION_WEB_CASE_TEMPLATE_INIT = """
{% if "create" in actions %}
from .create import CreateUseCase
{% endif %}
{% if "delete" in actions %}
from .delete import DeleteUseCase
{% endif %}
{% if "retrieve" in actions %}
from .retrieve import RetrieveUseCase
{% endif %}
{% if "list" in actions %}
from .list import ListUseCase
{% endif %}
{% if "update" in actions %}
from .update import UpdateUseCase
{% endif %}
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
    \"\"\"{{ action.capitalize() }} operation for {{ model_pascal_case }}.\"\"\"

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
        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.create(data=data)
        await self.unit_of_work.commit()
        return {{ model_snake_case }}

    {% elif action == "update" %}
    async def execute(self, *, {{ model_snake_case }}_id: int, data: Update{{ model_pascal_case }}Data) -> {{ model_pascal_case }}:
        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.update(
            id={{ model_snake_case }}_id,
            data=data,
        )
        await self.unit_of_work.commit()
        return {{ model_snake_case }}

    {% elif action == "list" %}
    async def execute(self, *, filter_params: FilterParams) -> tuple[list[{{ model_pascal_case }}], int]:
        return await self.{{ model_snake_case }}_repository.get(
            skip=filter_params.skip,
            limit=filter_params.limit,
            order_by=filter_params.order_by,
            search=filter_params.search,
        )

    {% elif action == "retrieve" %}
    async def execute(self, *, {{ model_snake_case }}_id: int) -> {{ model_pascal_case }}:
        return await self.{{ model_snake_case }}_repository.get_by_id(id={{ model_snake_case }}_id)

    {% elif action == "delete" %}
    async def execute(self, *, {{ model_snake_case }}_id: int) -> {{ model_pascal_case }}:
        {{ model_snake_case }} = await self.{{ model_snake_case }}_repository.delete(id={{ model_snake_case }}_id)
        await self.unit_of_work.commit()
        return {{ model_snake_case }}

    {% endif %}
"""
