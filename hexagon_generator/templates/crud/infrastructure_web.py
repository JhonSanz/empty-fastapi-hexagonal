INFRASTRUCTURE_WEB_TEMPLATE = """
from fastapi import APIRouter, Depends, Path, Query, status
from typing import Annotated
from sqlalchemy.orm import Session

from src.common.std_response import std_response, StandardResponse
from src.common.database_connection import get_db
from src.{{ model_snake_case }}.application.handlers import (
    create_handler,
    retrieve_handler,
    list_handler,
    update_handler,
    delete_handler
)
from src.{{ model_snake_case }}.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase
)
from src.{{ model_snake_case }}.application.schemas import (
    {{ model_pascal_case }}Response,
    {{ model_pascal_case }}ListResponse,
    Create{{ model_pascal_case }}Request,
    Update{{ model_pascal_case }}Request,
    FilterParams,
)
from src.{{ model_snake_case }}.infrastructure.database import ORM{{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.{{ model_snake_case }}.application.service import {{ model_pascal_case }}Service


router = APIRouter(
    prefix="/{{ model_snake_case }}",
    tags=["{{ model_pascal_case }}"],
)


# Dependency injection helpers
def get_{{ model_snake_case }}_repository(db: Session = Depends(get_db)) -> ORM{{ model_pascal_case }}Repository:
    \"\"\"Get {{ model_pascal_case }} repository instance.\"\"\"
    return ORM{{ model_pascal_case }}Repository(db=db)


def get_{{ model_snake_case }}_unit_of_work(db: Session = Depends(get_db)) -> SQLAlchemyUnitOfWork:
    \"\"\"Get Unit of Work instance.\"\"\"
    return SQLAlchemyUnitOfWork(session=db)


def get_{{ model_snake_case }}_service() -> {{ model_pascal_case }}Service:
    \"\"\"Get {{ model_pascal_case }} service instance.\"\"\"
    return {{ model_pascal_case }}Service()


{% for action in actions %}
{% if action == "create" %}
@router.post(
    "/",
    response_model=StandardResponse[{{ model_pascal_case }}Response],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new {{ model_pascal_case }}",
    description="Create a new {{ model_pascal_case }} with the provided data.",
    responses={
        201: {"description": "{{ model_pascal_case }} created successfully"},
        400: {"description": "Invalid input data"},
        422: {"description": "Validation error"},
    },
)
async def create_{{ model_snake_case }}(
    {{ model_snake_case }}_data: Create{{ model_pascal_case }}Request,
    unit_of_work: SQLAlchemyUnitOfWork = Depends(get_{{ model_snake_case }}_unit_of_work),
    repository: ORM{{ model_pascal_case }}Repository = Depends(get_{{ model_snake_case }}_repository),
    service: {{ model_pascal_case }}Service = Depends(get_{{ model_snake_case }}_service),
) -> StandardResponse[{{ model_pascal_case }}Response]:
    \"\"\"
    Create a new {{ model_pascal_case }}.

    Args:
        {{ model_snake_case }}_data: Data for creating the {{ model_pascal_case }}
        unit_of_work: Unit of Work for transaction management
        repository: {{ model_pascal_case }} repository
        service: {{ model_pascal_case }} service

    Returns:
        Created {{ model_pascal_case }} data
    \"\"\"
    create_use_case = CreateUseCase(
        unit_of_work=unit_of_work,
        {{ model_snake_case }}_repository=repository,
        {{ model_snake_case }}_service=service
    )
    result = await create_handler(
        create_{{ model_snake_case }}_request={{ model_snake_case }}_data,
        create_use_case=create_use_case
    )
    return std_response(data=result, status_code=status.HTTP_201_CREATED)


{% elif action == "list" %}
@router.get(
    "/",
    response_model=StandardResponse[list[{{ model_pascal_case }}ListResponse]],
    status_code=status.HTTP_200_OK,
    summary="List all {{ model_pascal_case }}s",
    description="Retrieve a paginated list of {{ model_pascal_case }}s with optional filtering.",
    responses={
        200: {"description": "List retrieved successfully"},
    },
)
async def list_{{ model_snake_case }}s(
    filter_params: Annotated[FilterParams, Query()],
    unit_of_work: SQLAlchemyUnitOfWork = Depends(get_{{ model_snake_case }}_unit_of_work),
    repository: ORM{{ model_pascal_case }}Repository = Depends(get_{{ model_snake_case }}_repository),
    service: {{ model_pascal_case }}Service = Depends(get_{{ model_snake_case }}_service),
) -> StandardResponse[list[{{ model_pascal_case }}ListResponse]]:
    \"\"\"
    Get a paginated list of {{ model_pascal_case }}s.

    Args:
        filter_params: Pagination and filter parameters
        unit_of_work: Unit of Work for transaction management
        repository: {{ model_pascal_case }} repository
        service: {{ model_pascal_case }} service

    Returns:
        List of {{ model_pascal_case }}s with pagination metadata
    \"\"\"
    list_use_case = ListUseCase(
        unit_of_work=unit_of_work,
        {{ model_snake_case }}_repository=repository,
        {{ model_snake_case }}_service=service
    )
    result, count = await list_handler(
        filter_params=filter_params,
        list_use_case=list_use_case
    )
    return std_response(data=result, count=count)


{% elif action == "retrieve" %}
@router.get(
    "/{{ '{' }}{{ model_snake_case }}_id}",
    response_model=StandardResponse[{{ model_pascal_case }}Response],
    status_code=status.HTTP_200_OK,
    summary="Get {{ model_pascal_case }} by ID",
    description="Retrieve a specific {{ model_pascal_case }} by its ID.",
    responses={
        200: {"description": "{{ model_pascal_case }} found"},
        404: {"description": "{{ model_pascal_case }} not found"},
    },
)
async def get_{{ model_snake_case }}(
    {{ model_snake_case }}_id: Annotated[
        int,
        Path(..., description="ID of the {{ model_pascal_case }} to retrieve", gt=0)
    ],
    unit_of_work: SQLAlchemyUnitOfWork = Depends(get_{{ model_snake_case }}_unit_of_work),
    repository: ORM{{ model_pascal_case }}Repository = Depends(get_{{ model_snake_case }}_repository),
    service: {{ model_pascal_case }}Service = Depends(get_{{ model_snake_case }}_service),
) -> StandardResponse[{{ model_pascal_case }}Response]:
    \"\"\"
    Get a {{ model_pascal_case }} by ID.

    Args:
        {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to retrieve
        unit_of_work: Unit of Work for transaction management
        repository: {{ model_pascal_case }} repository
        service: {{ model_pascal_case }} service

    Returns:
        {{ model_pascal_case }} data
    \"\"\"
    retrieve_use_case = RetrieveUseCase(
        unit_of_work=unit_of_work,
        {{ model_snake_case }}_repository=repository,
        {{ model_snake_case }}_service=service
    )
    result = await retrieve_handler(
        {{ model_snake_case }}_id={{ model_snake_case }}_id,
        retrieve_use_case=retrieve_use_case
    )
    return std_response(data=result)


{% elif action == "update" %}
@router.put(
    "/{{ '{' }}{{ model_snake_case }}_id}",
    response_model=StandardResponse[{{ model_pascal_case }}Response],
    status_code=status.HTTP_200_OK,
    summary="Update {{ model_pascal_case }}",
    description="Update an existing {{ model_pascal_case }} with new data.",
    responses={
        200: {"description": "{{ model_pascal_case }} updated successfully"},
        404: {"description": "{{ model_pascal_case }} not found"},
        400: {"description": "Invalid input data"},
        422: {"description": "Validation error"},
    },
)
async def update_{{ model_snake_case }}(
    {{ model_snake_case }}_id: Annotated[
        int,
        Path(..., description="ID of the {{ model_pascal_case }} to update", gt=0)
    ],
    {{ model_snake_case }}_data: Update{{ model_pascal_case }}Request,
    unit_of_work: SQLAlchemyUnitOfWork = Depends(get_{{ model_snake_case }}_unit_of_work),
    repository: ORM{{ model_pascal_case }}Repository = Depends(get_{{ model_snake_case }}_repository),
    service: {{ model_pascal_case }}Service = Depends(get_{{ model_snake_case }}_service),
) -> StandardResponse[{{ model_pascal_case }}Response]:
    \"\"\"
    Update a {{ model_pascal_case }}.

    Args:
        {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to update
        {{ model_snake_case }}_data: New data for the {{ model_pascal_case }}
        unit_of_work: Unit of Work for transaction management
        repository: {{ model_pascal_case }} repository
        service: {{ model_pascal_case }} service

    Returns:
        Updated {{ model_pascal_case }} data
    \"\"\"
    update_use_case = UpdateUseCase(
        unit_of_work=unit_of_work,
        {{ model_snake_case }}_repository=repository,
        {{ model_snake_case }}_service=service
    )
    result = await update_handler(
        {{ model_snake_case }}_id={{ model_snake_case }}_id,
        update_{{ model_snake_case }}_request={{ model_snake_case }}_data,
        update_use_case=update_use_case
    )
    return std_response(data=result)


{% elif action == "delete" %}
@router.delete(
    "/{{ '{' }}{{ model_snake_case }}_id}",
    response_model=StandardResponse[{{ model_pascal_case }}Response],
    status_code=status.HTTP_200_OK,
    summary="Delete {{ model_pascal_case }}",
    description="Delete a {{ model_pascal_case }} by its ID.",
    responses={
        200: {"description": "{{ model_pascal_case }} deleted successfully"},
        404: {"description": "{{ model_pascal_case }} not found"},
    },
)
async def delete_{{ model_snake_case }}(
    {{ model_snake_case }}_id: Annotated[
        int,
        Path(..., description="ID of the {{ model_pascal_case }} to delete", gt=0)
    ],
    unit_of_work: SQLAlchemyUnitOfWork = Depends(get_{{ model_snake_case }}_unit_of_work),
    repository: ORM{{ model_pascal_case }}Repository = Depends(get_{{ model_snake_case }}_repository),
    service: {{ model_pascal_case }}Service = Depends(get_{{ model_snake_case }}_service),
) -> StandardResponse[{{ model_pascal_case }}Response]:
    \"\"\"
    Delete a {{ model_pascal_case }}.

    Args:
        {{ model_snake_case }}_id: ID of the {{ model_pascal_case }} to delete
        unit_of_work: Unit of Work for transaction management
        repository: {{ model_pascal_case }} repository
        service: {{ model_pascal_case }} service

    Returns:
        Deleted {{ model_pascal_case }} data
    \"\"\"
    delete_use_case = DeleteUseCase(
        unit_of_work=unit_of_work,
        {{ model_snake_case }}_repository=repository,
        {{ model_snake_case }}_service=service
    )
    result = await delete_handler(
        {{ model_snake_case }}_id={{ model_snake_case }}_id,
        delete_use_case=delete_use_case
    )
    return std_response(data=result)


{% endif %}
{% endfor %}
"""
