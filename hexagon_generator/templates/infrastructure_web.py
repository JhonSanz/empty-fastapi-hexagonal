INFRASTRUCTURE_WEB_TEMPLATE = """
from fastapi import APIRouter, Depends, Query, status
from typing import Annotated
from src.common.std_response import std_response, StandardResponse
from src.common.database_connection import get_db
from sqlalchemy.orm import Session

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
    {{ model_pascal_case }}InDBBase,
    Create{{ model_pascal_case }}Request,
    Update{{ model_pascal_case }}Request,
    FilterParams,
)
from src.{{ model_snake_case }}.infrastructure.database import ORM{{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.application.service import {{ model_pascal_case }}Service


router = APIRouter()

{% for action in actions %}
{% if action == "create" %}
@router.post("/create", response_model=StandardResponse[{{ model_pascal_case }}InDBBase])
async def create_endpoint(
    create_{{ model_snake_case }}_request: Create{{ model_pascal_case }}Request,
    database: Session = Depends(get_db)
):
    {{ model_snake_case }}_repo = ORM{{ model_pascal_case }}Repository(db=database)
    {{ model_snake_case }}_service = {{ model_pascal_case }}Service()
    create_use_case = CreateUseCase(
        {{ model_snake_case }}_repository={{ model_snake_case }}_repo,
        {{ model_snake_case }}_service={{ model_snake_case }}_service
    )
    result = create_handler(
        create_{{ model_snake_case }}_request=create_{{ model_snake_case }}_request,
        create_use_case=create_use_case
    )
    return std_response(data=result)
{% elif action == "list" %}
@router.get("/list", response_model=StandardResponse[list[{{ model_pascal_case }}InDBBase]])
async def list_endpoint(
    filter_params: Annotated[FilterParams, Query()],
    database: Session = Depends(get_db)
):
    {{ model_snake_case }}_repo = ORM{{ model_pascal_case }}Repository(db=database)
    {{ model_snake_case }}_service = {{ model_pascal_case }}Service()
    list_use_case = ListUseCase(
        {{ model_snake_case }}_repository={{ model_snake_case }}_repo,
        {{ model_snake_case }}_service={{ model_snake_case }}_service
    )
    result, count = list_handler(
        filter_params=filter_params,
        list_use_case=list_use_case
    )
    return std_response(data=result, count=count)
{% elif action in ["retrieve", "delete"] %}
@router.{{ "get" if action == "retrieve" else "delete" }}("/{{ '{' }}{{ model_snake_case }}_id}/{{ action }}", response_model=StandardResponse[{{ model_pascal_case }}InDBBase])
async def {{ action }}_endpoint(
    {{ model_snake_case }}_id: int,
    database: Session = Depends(get_db)
):
    {{ model_snake_case }}_repo = ORM{{ model_pascal_case }}Repository(db=database)
    {{ model_snake_case }}_service = {{ model_pascal_case }}Service()
    {{ action }}_use_case = {{ action.capitalize() }}UseCase(
        {{ model_snake_case }}_repository={{ model_snake_case }}_repo,
        {{ model_snake_case }}_service={{ model_snake_case }}_service
    )
    result = {{ action }}_handler(
        {{ model_snake_case }}_id={{ model_snake_case }}_id,
        {{ action }}_use_case={{ action }}_use_case
    )
    return std_response(data=result)
{% elif action == "update" %}
@router.put("/{{ '{' }}{{ model_snake_case }}_id}/update", response_model=StandardResponse[{{ model_pascal_case }}InDBBase])
async def update_endpoint(
    {{ model_snake_case }}_id: int,
    update_{{ model_snake_case }}_request: Update{{ model_pascal_case }}Request,
    database: Session = Depends(get_db)
):
    {{ model_snake_case }}_repo = ORM{{ model_pascal_case }}Repository(db=database)
    {{ model_snake_case }}_service = {{ model_pascal_case }}Service()
    update_use_case = UpdateUseCase(
        {{ model_snake_case }}_repository={{ model_snake_case }}_repo,
        {{ model_snake_case }}_service={{ model_snake_case }}_service
    )
    result = update_handler(
        {{ model_snake_case }}_id={{ model_snake_case }}_id,
        update_{{ model_snake_case }}_request=update_{{ model_snake_case }}_request,
        update_use_case=update_use_case
    )
    return std_response(data=result)
{% endif %}
{% endfor %}

"""
