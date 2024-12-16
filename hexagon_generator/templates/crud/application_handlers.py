APPLICATION_HANDLERS_TEMPLATE = """
from src.{{ model_snake_case }}.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase
)
from src.{{ model_snake_case }}.application.schemas import (
    Create{{ model_pascal_case }}Request,
    Update{{ model_pascal_case }}Request,
    FilterParams,
)
from src.{{ model_snake_case }}.domain.models import {{ model_pascal_case }}

{% for action in actions %}
async def {{ action }}_handler(
    *,
    {% if action == "create" %}
    create_{{ model_snake_case }}_request: Create{{ model_pascal_case }}Request,
    create_use_case: CreateUseCase
    {% elif action == "update" %}
    {{ model_snake_case }}_id: int,
    update_{{ model_snake_case }}_request: Update{{ model_pascal_case }}Request,
    update_use_case: UpdateUseCase
    {% elif action == "retrieve" %}
    {{ model_snake_case }}_id: int,
    retrieve_use_case: RetrieveUseCase
    {% elif action == "list" %}
    filter_params: FilterParams,
    list_use_case: ListUseCase
    {% elif action == "delete" %}
    {{ model_snake_case }}_id: int,
    delete_use_case: DeleteUseCase
    {% endif %}
):
    {% if action == "create" %}
    data = await create_use_case.execute({{ model_snake_case }}_request=create_{{ model_snake_case }}_request)
    {% elif action == "update" %}
    data = await update_use_case.execute(
        {{ model_snake_case }}_id={{ model_snake_case }}_id,
        {{ model_snake_case }}_request=update_{{ model_snake_case }}_request
    )
    {% elif action == "retrieve" %}
    data = await retrieve_use_case.execute({{ model_snake_case }}_id={{ model_snake_case }}_id)
    {% elif action == "list" %}
    data, count = await list_use_case.execute(filter_params=filter_params)
    return data, count
    {% elif action == "delete" %}
    data = await delete_use_case.execute({{ model_snake_case }}_id={{ model_snake_case }}_id)
    {% endif %}
    {% if action != "list" %}
    return data
    {% endif %}
{% endfor %}

"""
