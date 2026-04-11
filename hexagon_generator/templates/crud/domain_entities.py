DOMAIN_ENTITIES_TEMPLATE = """
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class {{ model_pascal_case }}:
    \"\"\"{{ model_pascal_case }} domain entity.\"\"\"
    id: int
    # TODO: Add your domain fields here
    # Example:
    # name: str
    # description: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class Create{{ model_pascal_case }}Data:
    \"\"\"Data required to create a {{ model_pascal_case }}.\"\"\"
    # TODO: Add your fields here
    # Example:
    # name: str
    # description: Optional[str] = None
    pass


@dataclass
class Update{{ model_pascal_case }}Data:
    \"\"\"Data for updating a {{ model_pascal_case }}. All fields optional.\"\"\"
    # TODO: Add your fields here (all Optional)
    # Example:
    # name: Optional[str] = None
    # description: Optional[str] = None
    pass
"""
