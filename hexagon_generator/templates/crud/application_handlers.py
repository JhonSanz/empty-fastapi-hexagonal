APPLICATION_HANDLERS_TEMPLATE = """
\"\"\"
Handlers for {{ model_pascal_case }} operations.

This module contains handler functions that coordinate between
the web layer and use cases.
\"\"\"

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
{% if action == "create" %}
async def create_handler(
    *,
    create_{{ model_snake_case }}_request: Create{{ model_pascal_case }}Request,
    create_use_case: CreateUseCase
) -> {{ model_pascal_case }}:
    \"\"\"
    Handle {{ model_pascal_case }} creation.

    Args:
        create_{{ model_snake_case }}_request: Data for creating the {{ model_pascal_case }}
        create_use_case: Use case for creation logic

    Returns:
        Created {{ model_pascal_case }} instance
    \"\"\"
    return await create_use_case.execute({{ model_snake_case }}_request=create_{{ model_snake_case }}_request)


{% elif action == "retrieve" %}
async def retrieve_handler(
    *,
    {{ model_snake_case }}_id: int,
    retrieve_use_case: RetrieveUseCase
) -> {{ model_pascal_case }}:
    \"\"\"
    Handle {{ model_pascal_case }} retrieval by ID.

    Args:
        {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to retrieve
        retrieve_use_case: Use case for retrieval logic

    Returns:
        Retrieved {{ model_pascal_case }} instance
    \"\"\"
    return await retrieve_use_case.execute({{ model_snake_case }}_id={{ model_snake_case }}_id)


{% elif action == "list" %}
async def list_handler(
    *,
    filter_params: FilterParams,
    list_use_case: ListUseCase
) -> tuple[list[{{ model_pascal_case }}], int]:
    \"\"\"
    Handle {{ model_pascal_case }} list retrieval.

    Args:
        filter_params: Filtering and pagination parameters
        list_use_case: Use case for list logic

    Returns:
        Tuple of (list of {{ model_pascal_case }}s, total count)
    \"\"\"
    return await list_use_case.execute(filter_params=filter_params)


{% elif action == "update" %}
async def update_handler(
    *,
    {{ model_snake_case }}_id: int,
    update_{{ model_snake_case }}_request: Update{{ model_pascal_case }}Request,
    update_use_case: UpdateUseCase
) -> {{ model_pascal_case }}:
    \"\"\"
    Handle {{ model_pascal_case }} update.

    Args:
        {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to update
        update_{{ model_snake_case }}_request: New data for the {{ model_pascal_case }}
        update_use_case: Use case for update logic

    Returns:
        Updated {{ model_pascal_case }} instance
    \"\"\"
    return await update_use_case.execute(
        {{ model_snake_case }}_id={{ model_snake_case }}_id,
        {{ model_snake_case }}_request=update_{{ model_snake_case }}_request
    )


{% elif action == "delete" %}
async def delete_handler(
    *,
    {{ model_snake_case }}_id: int,
    delete_use_case: DeleteUseCase
) -> {{ model_pascal_case }}:
    \"\"\"
    Handle {{ model_pascal_case }} deletion.

    Args:
        {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to delete
        delete_use_case: Use case for deletion logic

    Returns:
        Deleted {{ model_pascal_case }} instance
    \"\"\"
    return await delete_use_case.execute({{ model_snake_case }}_id={{ model_snake_case }}_id)


{% endif %}
{% endfor %}
"""
