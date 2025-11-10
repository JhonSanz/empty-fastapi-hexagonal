INFRASTRUCTURE_DATABASE_TEMPLATE = """
from typing import Optional
from sqlalchemy import select, update, delete, func, or_, desc, asc
from sqlalchemy.orm import Session

from src.{{ model_snake_case }}.domain.repository import {{ model_pascal_case }}Repository
from src.{{ model_snake_case }}.domain.models import {{ model_pascal_case }}
from src.{{ model_snake_case }}.application.schemas import (
    Create{{ model_pascal_case }}Request,
    Update{{ model_pascal_case }}Request,
    FilterParams,
)
from src.{{ model_snake_case }}.domain.exceptions import {{ model_pascal_case }}NotFoundException


class ORM{{ model_pascal_case }}Repository({{ model_pascal_case }}Repository):
    \"\"\"SQLAlchemy implementation of {{ model_pascal_case }}Repository using SQLAlchemy 2.0 style.\"\"\"

    def __init__(self, *, db: Session):
        self.db = db

    async def get_by_id(self, *, id: int) -> {{ model_pascal_case }}:
        \"\"\"
        Get a {{ model_pascal_case }} by ID.

        Args:
            id: ID of the {{ model_pascal_case }}

        Returns:
            {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"\"\"
        stmt = select({{ model_pascal_case }}).where({{ model_pascal_case }}.id == id)
        result = self.db.execute(stmt)
        {{ model_snake_case }} = result.scalar_one_or_none()

        if not {{ model_snake_case }}:
            raise {{ model_pascal_case }}NotFoundException(f"{{ model_pascal_case }} with ID {id} not found")

        return {{ model_snake_case }}

    async def get(self, *, filter_params: FilterParams) -> tuple[list[{{ model_pascal_case }}], int]:
        \"\"\"
        Get a list of {{ model_pascal_case }}s with filtering and pagination.

        Args:
            filter_params: Filtering and pagination parameters

        Returns:
            Tuple of (list of {{ model_pascal_case }}s, total count)
        \"\"\"
        # Base query
        stmt = select({{ model_pascal_case }})

        # Apply search filter if provided
        if filter_params.search:
            # TODO: Customize search fields based on your model
            search_pattern = f"%{filter_params.search}%"
            stmt = stmt.where(
                or_(
                    # Example search fields - customize based on your model
                    # {{ model_pascal_case }}.name.ilike(search_pattern),
                    # {{ model_pascal_case }}.description.ilike(search_pattern),
                )
            )

        # TODO: Add custom filters based on filter_params
        # Example:
        # if filter_params.status:
        #     stmt = stmt.where({{ model_pascal_case }}.status == filter_params.status)

        # Get total count before pagination
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count = self.db.execute(count_stmt).scalar()

        # Apply ordering
        if filter_params.order_by:
            order_field = filter_params.order_by.lstrip('-')
            is_desc = filter_params.order_by.startswith('-')

            # TODO: Add validation for allowed order fields
            if hasattr({{ model_pascal_case }}, order_field):
                order_column = getattr({{ model_pascal_case }}, order_field)
                stmt = stmt.order_by(desc(order_column) if is_desc else asc(order_column))
        else:
            # Default ordering
            stmt = stmt.order_by(desc({{ model_pascal_case }}.id))

        # Apply pagination
        stmt = stmt.offset(filter_params.skip).limit(filter_params.limit)

        # Execute query
        result = self.db.execute(stmt)
        {{ model_snake_case }}s = result.scalars().all()

        return list({{ model_snake_case }}s), count

    async def create(self, *, data: Create{{ model_pascal_case }}Request) -> {{ model_pascal_case }}:
        \"\"\"
        Create a new {{ model_pascal_case }}.

        Args:
            data: Data for creating the {{ model_pascal_case }}

        Returns:
            Created {{ model_pascal_case }} instance
        \"\"\"
        data_dict = data.model_dump()
        {{ model_snake_case }} = {{ model_pascal_case }}(**data_dict)

        self.db.add({{ model_snake_case }})
        self.db.flush()
        self.db.refresh({{ model_snake_case }})

        return {{ model_snake_case }}

    async def update(self, *, id: int, data: Update{{ model_pascal_case }}Request) -> {{ model_pascal_case }}:
        \"\"\"
        Update an existing {{ model_pascal_case }}.

        Args:
            id: ID of the {{ model_pascal_case }} to update
            data: New data for the {{ model_pascal_case }}

        Returns:
            Updated {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"\"\"
        # First check if {{ model_pascal_case }} exists
        await self.get_by_id(id=id)

        # Prepare update data (exclude None values for partial updates)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            # No fields to update, just return the existing {{ model_snake_case }}
            return await self.get_by_id(id=id)

        # Perform update
        stmt = (
            update({{ model_pascal_case }})
            .where({{ model_pascal_case }}.id == id)
            .values(**update_data)
        )
        self.db.execute(stmt)
        self.db.flush()

        # Return updated {{ model_snake_case }}
        return await self.get_by_id(id=id)

    async def delete(self, *, id: int) -> {{ model_pascal_case }}:
        \"\"\"
        Delete a {{ model_pascal_case }}.

        Args:
            id: ID of the {{ model_pascal_case }} to delete

        Returns:
            Deleted {{ model_pascal_case }} instance

        Raises:
            {{ model_pascal_case }}NotFoundException: If {{ model_pascal_case }} not found
        \"\"\"
        # First get the {{ model_snake_case }} to return it and ensure it exists
        {{ model_snake_case }} = await self.get_by_id(id=id)

        # Delete the {{ model_snake_case }}
        stmt = delete({{ model_pascal_case }}).where({{ model_pascal_case }}.id == id)
        self.db.execute(stmt)
        self.db.flush()

        return {{ model_snake_case }}
"""
