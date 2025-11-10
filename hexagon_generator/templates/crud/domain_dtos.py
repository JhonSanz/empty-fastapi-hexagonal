DOMAIN_DTOS_TEMPLATE = """
\"\"\"
Domain Data Transfer Objects for {{ model_pascal_case }}.

These are simple dataclasses used by the domain layer.
No external dependencies (Pydantic, SQLAlchemy, etc).
\"\"\"

from dataclasses import dataclass
from typing import Optional


@dataclass
class Create{{ model_pascal_case }}DTO:
    \"\"\"DTO for creating a {{ model_pascal_case }}.\"\"\"
    # TODO: Add your domain fields here
    # Example:
    # name: str
    # description: Optional[str] = None
    pass


@dataclass
class Update{{ model_pascal_case }}DTO:
    \"\"\"DTO for updating a {{ model_pascal_case }}.\"\"\"
    # TODO: Add fields that can be updated (all optional)
    # Example:
    # name: Optional[str] = None
    # description: Optional[str] = None
    pass


@dataclass
class {{ model_pascal_case }}FilterDTO:
    \"\"\"DTO for filtering {{ model_pascal_case }}s.\"\"\"
    skip: int = 0
    limit: int = 10
    order_by: Optional[str] = None
    search: Optional[str] = None

    # TODO: Add specific filters for your domain
    # Example:
    # status: Optional[str] = None
    # created_after: Optional[datetime] = None
"""
