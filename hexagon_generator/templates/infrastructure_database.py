INFRASTRUCTURE_DATABASE_TEMPLATE = """
from src.{{ model_snake_case }}.domain.repository import {{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.domain.models import {{ model_pascal_case }}
from src.{{ model_snake_case }}.application.schemas import (
    {{ model_pascal_case }}InDBBase,
    Create{{ model_pascal_case }}Request,
    Update{{ model_pascal_case }}Request,
    FilterParams,
)
from src.{{ model_snake_case }}.domain.exceptions import {{ model_pascal_case }}NotFoundException 


class ORM{{ model_pascal_case }}Repository({{ model_pascal_case }}Repository):
    def __init__(self, *, db):
        self.db = db

    async def get_by_id(self, *, id: int) -> {{ model_pascal_case }}:
        existing_{{ model_snake_case }} = (
            self.db.query({{ model_pascal_case }}).filter({{ model_pascal_case }}.id == id).first()
        )
        if not existing_{{ model_snake_case }}:
            raise {{ model_pascal_case }}NotFoundException(f"{{ model_pascal_case }} {id} not found")
        return existing_{{ model_snake_case }}

    async def get(self, *, filter_params: FilterParams) -> tuple[list[{{ model_pascal_case }}], int]:
        filters_ = {}
        {{ model_snake_case }}_query = (
            self.db.query({{ model_pascal_case }}).filter_by(**filters_).order_by({{ model_pascal_case }}.id.desc())
        )
        count = {{ model_snake_case }}_query.count()
        {{ model_snake_case }} = {{ model_snake_case }}_query.offset(filter_params.skip).limit(filter_params.limit).all()
        return {{ model_snake_case }}, count

    async def create(self, *, data: Create{{ model_pascal_case }}Request):
        {{ model_snake_case }}_result = {{ model_pascal_case }}(**data)
        self.db.add({{ model_snake_case }}_result)
        self.db.flush()
        self.db.refresh({{ model_snake_case }}_result)
        return {{ model_snake_case }}_result

    async def update(self, *, id: int, data: Update{{ model_pascal_case }}Request):
        {{ model_snake_case }}_result = (
            self.db.query({{ model_pascal_case }})
            .filter({{ model_pascal_case }}.id == id)
            .update(data, synchronize_session="fetch")
        )

        if {{ model_snake_case }}_result == 0:
            raise {{ model_pascal_case }}NotFoundException(f"{{ model_pascal_case }} with ID {id} not found")

        updated_{{ model_snake_case }} = (
            self.db.query({{ model_pascal_case }}).filter({{ model_pascal_case }}.id == id).first()
        )
        self.db.refresh(updated_{{ model_snake_case }})
        return updated_{{ model_snake_case }}

    async def delete(self, *, id: int):
        # TODO:
        pass
"""
