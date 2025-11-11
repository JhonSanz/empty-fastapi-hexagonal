"""Specialized prompts for completing TODOs in different file types."""

from typing import Any


def get_domain_dto_prompt(
    file_path: str,
    file_content: str,
    context: str,
    todos: list[dict[str, Any]]
) -> str:
    """Generate prompt for completing Domain DTOs.

    Args:
        file_path: Path to the file
        file_content: Content of the file
        context: Additional domain context
        todos: List of TODO items

    Returns:
        Completion prompt for LLM
    """
    return f"""You are completing TODOs in a Domain DTO file following hexagonal architecture principles.

File: {file_path}
Layer: Domain
Type: DTOs (Data Transfer Objects)

CONTEXT:
{context if context else "No additional context provided"}

HEXAGONAL ARCHITECTURE RULES FOR DOMAIN DTOs:
1. Domain DTOs are simple dataclasses with NO external dependencies
2. Use only Python built-in types: str, int, float, bool, datetime, UUID, etc.
3. NO Pydantic models, NO SQLAlchemy, NO FastAPI
4. These represent pure domain concepts
5. Include only business-relevant fields
6. Use descriptive field names in snake_case
7. Add type hints for all fields
8. Can include optional docstrings for clarity

CURRENT FILE CONTENT:
```python
{file_content}
```

TODOs TO COMPLETE:
{_format_todos(todos)}

INSTRUCTIONS:
1. Analyze the entity name and context to determine appropriate fields
2. Define fields using dataclass syntax with type hints
3. Consider common domain concepts: identifiers, names, descriptions, timestamps, status, etc.
4. Keep it simple - this is the domain layer
5. Return the COMPLETE file content with TODOs replaced by actual field definitions

Generate the completed file content now:"""


def get_domain_model_prompt(
    file_path: str,
    file_content: str,
    context: str,
    todos: list[dict[str, Any]]
) -> str:
    """Generate prompt for completing Domain Models (SQLAlchemy).

    Args:
        file_path: Path to the file
        file_content: Content of the file
        context: Additional domain context
        todos: List of TODO items

    Returns:
        Completion prompt for LLM
    """
    return f"""You are completing TODOs in a Domain Model file using SQLAlchemy 2.0.

File: {file_path}
Layer: Domain
Type: Models (SQLAlchemy ORM)

CONTEXT:
{context if context else "No additional context provided"}

SQLALCHEMY 2.0 BEST PRACTICES:
1. Use Mapped[] type hints for all columns
2. Use mapped_column() for column definitions
3. Include proper field types: Mapped[int], Mapped[str], Mapped[datetime], etc.
4. Add nullable with Mapped[Optional[...]] syntax
5. Define relationships using relationship() with proper back_populates
6. Use snake_case for table names (__tablename__)
7. Include common fields: id (PK), created_at, updated_at
8. Add indexes and constraints where appropriate

CURRENT FILE CONTENT:
```python
{file_content}
```

TODOs TO COMPLETE:
{_format_todos(todos)}

INSTRUCTIONS:
1. Define appropriate columns based on entity name and context
2. Include standard fields: id, created_at, updated_at
3. Add business-specific fields with proper types
4. Consider relationships if multiple entities exist
5. Use SQLAlchemy 2.0 Mapped syntax exclusively
6. Return the COMPLETE file content with TODOs replaced

Generate the completed file content now:"""


def get_schema_prompt(
    file_path: str,
    file_content: str,
    context: str,
    todos: list[dict[str, Any]]
) -> str:
    """Generate prompt for completing Pydantic Schemas.

    Args:
        file_path: Path to the file
        file_content: Content of the file
        context: Additional domain context
        todos: List of TODO items

    Returns:
        Completion prompt for LLM
    """
    return f"""You are completing TODOs in a Pydantic Schema file for FastAPI.

File: {file_path}
Layer: Application
Type: Schemas (Pydantic)

CONTEXT:
{context if context else "No additional context provided"}

PYDANTIC V2 BEST PRACTICES:
1. Use Field() for validations and examples
2. Separate Request and Response schemas (CreateXRequest, XResponse)
3. Add model_config with ConfigDict for ORM mode
4. Include field validations: min_length, max_length, ge, le, regex, etc.
5. Add examples for OpenAPI documentation
6. Use proper type hints: str, int, datetime, UUID, Optional, etc.
7. Include helpful descriptions in Field()
8. Response schemas should include id and timestamps

CURRENT FILE CONTENT:
```python
{file_content}
```

TODOs TO COMPLETE:
{_format_todos(todos)}

INSTRUCTIONS:
1. Define Request schemas with validations for input data
2. Define Response schemas for API responses (include id, timestamps)
3. Add Field() with proper constraints and examples
4. Ensure schemas match the domain model structure
5. Include helpful descriptions for API documentation
6. Return the COMPLETE file content with TODOs replaced

Generate the completed file content now:"""


def get_repository_prompt(
    file_path: str,
    file_content: str,
    context: str,
    todos: list[dict[str, Any]]
) -> str:
    """Generate prompt for completing Repository implementations.

    Args:
        file_path: Path to the file
        file_content: Content of the file
        context: Additional domain context
        todos: List of TODO items

    Returns:
        Completion prompt for LLM
    """
    return f"""You are completing TODOs in a Repository implementation using SQLAlchemy.

File: {file_path}
Layer: Infrastructure
Type: Repository (Database)

CONTEXT:
{context if context else "No additional context provided"}

REPOSITORY BEST PRACTICES:
1. Use SQLAlchemy 2.0 select() statements (NOT query())
2. Handle Domain DTOs, not Pydantic schemas
3. Convert DTOs to models using asdict()
4. Implement proper filtering with where() clauses
5. Add ordering with order_by()
6. Include pagination with limit() and offset()
7. Use scalars() for single results, all() for lists
8. Handle exceptions appropriately

CURRENT FILE CONTENT:
```python
{file_content}
```

TODOs TO COMPLETE:
{_format_todos(todos)}

INSTRUCTIONS:
1. Implement custom query methods if needed (e.g., find_by_name, find_active)
2. Add filtering logic based on common use cases
3. Use select() with where() for queries
4. Include proper type hints
5. Handle edge cases (not found, duplicates, etc.)
6. Return the COMPLETE file content with TODOs replaced

Generate the completed file content now:"""


def get_use_case_prompt(
    file_path: str,
    file_content: str,
    context: str,
    todos: list[dict[str, Any]]
) -> str:
    """Generate prompt for completing Use Case implementations.

    Args:
        file_path: Path to the file
        file_content: Content of the file
        context: Additional domain context
        todos: List of TODO items

    Returns:
        Completion prompt for LLM
    """
    return f"""You are completing TODOs in a Use Case file following hexagonal architecture.

File: {file_path}
Layer: Application
Type: Use Cases (Business Logic)

CONTEXT:
{context if context else "No additional context provided"}

USE CASE BEST PRACTICES:
1. Use cases coordinate between repositories and domain logic
2. Use UnitOfWork for transaction management
3. Handle business validations and rules
4. Raise appropriate exceptions (ValueError, HTTPException, etc.)
5. Keep use cases focused on a single responsibility
6. Use mappers to convert between layers
7. Return appropriate responses

CURRENT FILE CONTENT:
```python
{file_content}
```

TODOs TO COMPLETE:
{_format_todos(todos)}

INSTRUCTIONS:
1. Add business validation logic if needed
2. Implement error handling for common cases
3. Check for duplicates before creating
4. Verify existence before updating/deleting
5. Add any business rules specific to the domain
6. Use unit_of_work.commit() for persistence
7. Return the COMPLETE file content with TODOs replaced

Generate the completed file content now:"""


def _format_todos(todos: list[dict[str, Any]]) -> str:
    """Format TODO list for display in prompt.

    Args:
        todos: List of TODO items

    Returns:
        Formatted string
    """
    if not todos:
        return "No TODOs found"

    formatted = []
    for i, todo in enumerate(todos, 1):
        formatted.append(
            f"{i}. Line {todo['line_number']}: {todo['content']}"
        )

    return "\n".join(formatted)
