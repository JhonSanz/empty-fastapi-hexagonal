APPLICATION_WEB_CASE_TEMPLATE_INIT = """
from .create import CreateUseCase
from .delete import DeleteUseCase
from .retrieve import RetrieveUseCase
from .list import ListUseCase
from .update import UpdateUseCase
"""

APPLICATION_WEB_CASE_TEMPLATE = """from src.{{ model_snake_case }}.domain.repository import {{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.domain.exceptions import {{ model_pascal_case }}NotFoundException
from src.{{ model_snake_case }}.domain.models import {{ model_pascal_case }}
from src.{{ model_snake_case }}.application.interfaces import {{ model_pascal_case }}ServiceInterface
{% if action in ["create", "update"] %}
from src.{{ model_snake_case }}.application.schemas import {{ action.capitalize() }}{{ model_pascal_case }}Request
{% endif %}
{% if action == "list" %}
from src.{{ model_snake_case }}.application.schemas import FilterParams
{% endif %}

class {{ action.capitalize() }}UseCase:
    def __init__(
        self, *, {{ model_snake_case }}_repository: {{ model_pascal_case }}Repository, {{ model_snake_case }}_service: {{ model_pascal_case }}ServiceInterface
    ):
        self.{{ model_snake_case }}_repository = {{ model_snake_case }}_repository
        self.{{ model_snake_case }}_service = {{ model_snake_case }}_service

    {% if action == "create" %}
    def execute(self, *, {{ model_snake_case }}_request: {{ action.capitalize() }}{{ model_pascal_case }}Request) -> None:
        # TODO: your logic here
        self.{{ model_snake_case }}_repository.create(data={{ model_snake_case }}_request)
        return
    {% elif action == "update" %}
    def execute(self, *, {{ model_snake_case }}_id: int, {{ model_snake_case }}_request: {{ action.capitalize() }}{{ model_pascal_case }}Request) -> None:
        # TODO: your logic here
        self.{{ model_snake_case }}_repository.update(id={{ model_snake_case }}_id, data={{ model_snake_case }}_request)
        return
    {% elif action == "list" %}
    def execute(self, *, filter_params: FilterParams) -> tuple[list[{{ model_pascal_case }}], int]:
        # TODO: your logic here
        data, count = self.{{ model_snake_case }}_repository.get(filter_params=filter_params)
        return data, count
    {% elif action == "retrieve" %}
    def execute(self, *, {{ model_snake_case }}_id: int) -> {{ model_pascal_case }}:
        # TODO: your logic here
        data = self.{{ model_snake_case }}_repository.get_by_id(id={{ model_snake_case }}_id)
        return data
    {% elif action == "delete" %}
    def execute(self, *, {{ model_snake_case }}_id: int) -> None:
        # TODO: your logic here
        self.{{ model_snake_case }}_repository.delete(id={{ model_snake_case }}_id)
        return
    {% endif %}
"""
