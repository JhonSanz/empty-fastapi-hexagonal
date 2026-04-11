INFRASTRUCTURE_DATABASE_TEMPLATE = """
from dataclasses import asdict
from sqlalchemy import select, update, delete, func, or_, desc, asc
from sqlalchemy.orm import Session

from src.{{ model_snake_case }}.domain.repository import {{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.domain.entities import (
    {{ model_pascal_case }},
    Create{{ model_pascal_case }}Data,
    Update{{ model_pascal_case }}Data,
)
from src.{{ model_snake_case }}.domain.exceptions import {{ model_pascal_case }}NotFoundException
from src.{{ model_snake_case }}.infrastructure.models import {{ model_pascal_case }}ORM


class ORM{{ model_pascal_case }}Repository({{ model_pascal_case }}Repository):
    \"\"\"SQLAlchemy implementation of {{ model_pascal_case }}Repository.\"\"\"

    def __init__(self, *, db: Session):
        self.db = db

    @staticmethod
    def _to_entity(orm_obj: {{ model_pascal_case }}ORM) -> {{ model_pascal_case }}:
        \"\"\"Convert ORM model to domain entity.\"\"\"
        return {{ model_pascal_case }}(
            id=orm_obj.id,
            # TODO: Map your fields here
            # name=orm_obj.name,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    async def get_by_id(self, *, id: int) -> {{ model_pascal_case }}:
        stmt = select({{ model_pascal_case }}ORM).where({{ model_pascal_case }}ORM.id == id)
        result = self.db.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if not orm_obj:
            raise {{ model_pascal_case }}NotFoundException(f"{{ model_pascal_case }} with ID {id} not found")

        return self._to_entity(orm_obj)

    async def get(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        search: str | None = None,
        **filters,
    ) -> tuple[list[{{ model_pascal_case }}], int]:
        stmt = select({{ model_pascal_case }}ORM)

        if search:
            # TODO: Customize search fields based on your model
            search_pattern = f"%{search}%"
            stmt = stmt.where(
                or_(
                    # {{ model_pascal_case }}ORM.name.ilike(search_pattern),
                )
            )

        # TODO: Apply custom filters from **filters
        # Example:
        # if status := filters.get("status"):
        #     stmt = stmt.where({{ model_pascal_case }}ORM.status == status)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        count = self.db.execute(count_stmt).scalar()

        if order_by:
            order_field = order_by.lstrip("-")
            is_desc = order_by.startswith("-")

            if hasattr({{ model_pascal_case }}ORM, order_field):
                order_column = getattr({{ model_pascal_case }}ORM, order_field)
                stmt = stmt.order_by(desc(order_column) if is_desc else asc(order_column))
        else:
            stmt = stmt.order_by(desc({{ model_pascal_case }}ORM.id))

        stmt = stmt.offset(skip).limit(limit)

        result = self.db.execute(stmt)
        orm_objects = result.scalars().all()

        return [self._to_entity(obj) for obj in orm_objects], count

    async def create(self, *, data: Create{{ model_pascal_case }}Data) -> {{ model_pascal_case }}:
        data_dict = asdict(data)
        orm_obj = {{ model_pascal_case }}ORM(**data_dict)

        self.db.add(orm_obj)
        self.db.flush()
        self.db.refresh(orm_obj)

        return self._to_entity(orm_obj)

    async def update(self, *, id: int, data: Update{{ model_pascal_case }}Data) -> {{ model_pascal_case }}:
        await self.get_by_id(id=id)

        update_data = {k: v for k, v in asdict(data).items() if v is not None}

        if not update_data:
            return await self.get_by_id(id=id)

        stmt = (
            update({{ model_pascal_case }}ORM)
            .where({{ model_pascal_case }}ORM.id == id)
            .values(**update_data)
        )
        self.db.execute(stmt)
        self.db.flush()

        return await self.get_by_id(id=id)

    async def delete(self, *, id: int) -> {{ model_pascal_case }}:
        entity = await self.get_by_id(id=id)

        stmt = delete({{ model_pascal_case }}ORM).where({{ model_pascal_case }}ORM.id == id)
        self.db.execute(stmt)
        self.db.flush()

        return entity
"""
