INFRASTRUCTURE_WEB_TEMPLATE = """
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from src.common.std_response import std_response, StandardResponse
from src.common.database_connection import get_db
from src.{{ model_snake_case }}.domain.entities import (
    Create{{ model_pascal_case }}Data,
    Update{{ model_pascal_case }}Data,
)
from src.{{ model_snake_case }}.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase,
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


router = APIRouter(
    prefix="/{{ model_snake_case }}",
    tags=["{{ model_pascal_case }}"],
)


# --- Dependencies ---

def get_repository(db: Session = Depends(get_db)) -> ORM{{ model_pascal_case }}Repository:
    return ORM{{ model_pascal_case }}Repository(db=db)


def get_unit_of_work(db: Session = Depends(get_db)) -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(session=db)


Repository = Annotated[ORM{{ model_pascal_case }}Repository, Depends(get_repository)]
UoW = Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)]
{{ model_pascal_case }}Id = Annotated[int, Path(..., description="ID of the {{ model_pascal_case }}", gt=0)]


{% for action in actions %}
{% if action == "create" %}
@router.post(
    "/",
    response_model=StandardResponse[{{ model_pascal_case }}Response],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new {{ model_pascal_case }}",
    responses={
        201: {"description": "{{ model_pascal_case }} created successfully"},
        422: {"description": "Validation error"},
    },
)
async def create_{{ model_snake_case }}(
    {{ model_snake_case }}_data: Create{{ model_pascal_case }}Request,
    repository: Repository,
    unit_of_work: UoW,
) -> StandardResponse[{{ model_pascal_case }}Response]:
    data = Create{{ model_pascal_case }}Data(**{{ model_snake_case }}_data.model_dump())
    use_case = CreateUseCase(unit_of_work=unit_of_work, {{ model_snake_case }}_repository=repository)
    result = await use_case.execute(data=data)
    return std_response(data=result, status_code=status.HTTP_201_CREATED)


{% elif action == "list" %}
@router.get(
    "/",
    response_model=StandardResponse[list[{{ model_pascal_case }}ListResponse]],
    status_code=status.HTTP_200_OK,
    summary="List all {{ model_pascal_case }}s",
)
async def list_{{ model_snake_case }}s(
    filter_params: Annotated[FilterParams, Query()],
    repository: Repository,
    unit_of_work: UoW,
) -> StandardResponse[list[{{ model_pascal_case }}ListResponse]]:
    use_case = ListUseCase(unit_of_work=unit_of_work, {{ model_snake_case }}_repository=repository)
    result, count = await use_case.execute(filter_params=filter_params)
    return std_response(data=result, count=count)


{% elif action == "retrieve" %}
@router.get(
    "/{{ '{' }}{{ model_snake_case }}_id}",
    response_model=StandardResponse[{{ model_pascal_case }}Response],
    status_code=status.HTTP_200_OK,
    summary="Get {{ model_pascal_case }} by ID",
    responses={
        200: {"description": "{{ model_pascal_case }} found"},
        404: {"description": "{{ model_pascal_case }} not found"},
    },
)
async def get_{{ model_snake_case }}(
    {{ model_snake_case }}_id: {{ model_pascal_case }}Id,
    repository: Repository,
    unit_of_work: UoW,
) -> StandardResponse[{{ model_pascal_case }}Response]:
    use_case = RetrieveUseCase(unit_of_work=unit_of_work, {{ model_snake_case }}_repository=repository)
    result = await use_case.execute({{ model_snake_case }}_id={{ model_snake_case }}_id)
    return std_response(data=result)


{% elif action == "update" %}
@router.patch(
    "/{{ '{' }}{{ model_snake_case }}_id}",
    response_model=StandardResponse[{{ model_pascal_case }}Response],
    status_code=status.HTTP_200_OK,
    summary="Update {{ model_pascal_case }}",
    responses={
        200: {"description": "{{ model_pascal_case }} updated successfully"},
        404: {"description": "{{ model_pascal_case }} not found"},
        422: {"description": "Validation error"},
    },
)
async def update_{{ model_snake_case }}(
    {{ model_snake_case }}_id: {{ model_pascal_case }}Id,
    {{ model_snake_case }}_data: Update{{ model_pascal_case }}Request,
    repository: Repository,
    unit_of_work: UoW,
) -> StandardResponse[{{ model_pascal_case }}Response]:
    data = Update{{ model_pascal_case }}Data(**{{ model_snake_case }}_data.model_dump(exclude_none=True))
    use_case = UpdateUseCase(unit_of_work=unit_of_work, {{ model_snake_case }}_repository=repository)
    result = await use_case.execute({{ model_snake_case }}_id={{ model_snake_case }}_id, data=data)
    return std_response(data=result)


{% elif action == "delete" %}
@router.delete(
    "/{{ '{' }}{{ model_snake_case }}_id}",
    response_model=StandardResponse[{{ model_pascal_case }}Response],
    status_code=status.HTTP_200_OK,
    summary="Delete {{ model_pascal_case }}",
    responses={
        200: {"description": "{{ model_pascal_case }} deleted successfully"},
        404: {"description": "{{ model_pascal_case }} not found"},
    },
)
async def delete_{{ model_snake_case }}(
    {{ model_snake_case }}_id: {{ model_pascal_case }}Id,
    repository: Repository,
    unit_of_work: UoW,
) -> StandardResponse[{{ model_pascal_case }}Response]:
    use_case = DeleteUseCase(unit_of_work=unit_of_work, {{ model_snake_case }}_repository=repository)
    result = await use_case.execute({{ model_snake_case }}_id={{ model_snake_case }}_id)
    return std_response(data=result)


{% endif %}
{% endfor %}
"""
