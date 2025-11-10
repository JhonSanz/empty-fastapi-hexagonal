APPLICATION_SCHEMAS_TEMPLATE = """
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# Base schema with common fields
class {{ model_pascal_case }}Base(BaseModel):
    \"\"\"Base schema for {{ model_pascal_case }} with common fields.\"\"\"
    # TODO: Add your model fields here
    # Example:
    # name: str = Field(..., min_length=1, max_length=100, description="Name of the {{ model_pascal_case }}")
    # description: Optional[str] = Field(None, max_length=500, description="Description")
    pass


# Request schemas
class Create{{ model_pascal_case }}Request({{ model_pascal_case }}Base):
    \"\"\"Schema for creating a new {{ model_pascal_case }}.\"\"\"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                # TODO: Add example data
                # "name": "Example {{ model_pascal_case }}",
                # "description": "This is an example"
            }
        }
    )


class Update{{ model_pascal_case }}Request(BaseModel):
    \"\"\"Schema for updating an existing {{ model_pascal_case }}.\"\"\"
    # TODO: Add fields that can be updated (all optional for partial updates)
    # Example:
    # name: Optional[str] = Field(None, min_length=1, max_length=100)
    # description: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                # TODO: Add example data
                # "name": "Updated {{ model_pascal_case }}",
            }
        }
    )


# Response schemas
class {{ model_pascal_case }}Response({{ model_pascal_case }}Base):
    \"\"\"Schema for {{ model_pascal_case }} responses (full detail).\"\"\"

    id: int = Field(..., description="{{ model_pascal_case }} unique identifier", gt=0)
    created_at: datetime = Field(..., description="Timestamp when the {{ model_pascal_case }} was created")
    updated_at: datetime = Field(..., description="Timestamp when the {{ model_pascal_case }} was last updated")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                # TODO: Add your fields
                # "name": "Example {{ model_pascal_case }}",
                # "description": "This is an example",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }
    )


class {{ model_pascal_case }}ListResponse(BaseModel):
    \"\"\"Schema for {{ model_pascal_case }} in list responses (summary view).\"\"\"

    id: int = Field(..., description="{{ model_pascal_case }} unique identifier", gt=0)
    # TODO: Add main fields for list view (keep it minimal)
    # Example:
    # name: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                # TODO: Add your fields
                # "name": "Example {{ model_pascal_case }}",
                "created_at": "2024-01-15T10:30:00"
            }
        }
    )


# Filter and pagination schemas
class FilterParams(BaseModel):
    \"\"\"Schema for filtering and pagination parameters.\"\"\"

    skip: int = Field(
        default=0,
        ge=0,
        description="Number of records to skip (for pagination)"
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of records to return"
    )
    order_by: Optional[str] = Field(
        default="id",
        description="Field to order by (prefix with '-' for descending)"
    )
    search: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Search term to filter results"
    )

    # TODO: Add specific filters for your model
    # Example:
    # status: Optional[str] = Field(None, description="Filter by status")
    # created_after: Optional[datetime] = Field(None, description="Filter by creation date")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "skip": 0,
                "limit": 10,
                "order_by": "-created_at",
                "search": "example"
            }
        }
    )

"""
