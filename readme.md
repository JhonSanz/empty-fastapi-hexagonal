# Hexagonal Architecture Generator for FastAPI

Generate FastAPI CRUD modules following hexagonal (ports & adapters) architecture principles.

## Features

- **Complete CRUD Generation**: Generate domain models, DTOs, repositories, use cases, schemas, and API routes
- **Hexagonal Architecture**: Enforces proper layer separation (Domain, Application, Infrastructure)
- **SQLAlchemy 2.0**: Uses modern Mapped types and select() statements
- **Pydantic V2**: Includes Field validations and OpenAPI documentation
- **Unit of Work Pattern**: Transaction management abstraction
- **Architecture Validation**: Check compliance with hexagonal principles

## Quick Start

### Installation

```bash
pip install -e .
```

### CLI Usage

```bash
# Generate a CRUD module (always written under ./generated_project)
python code_generator.py crud School

# Generate CRUD with specific actions
python code_generator.py crud Product --actions create list retrieve

# Copy a built-in application
python code_generator.py builtin user

# Verbose output
python code_generator.py crud Order -v
```

## Generated Structure

```
generated_project/
└── src/
    └── school/
        ├── domain/                    # Business logic & entities
        │   ├── entities.py            # Domain entity + Create/Update DTOs (dataclasses)
        │   ├── exceptions.py          # Domain-level exceptions
        │   ├── repository.py          # Repository interface (port)
        │   └── unit_of_work.py        # Transaction interface (port)
        ├── application/                # Use cases & orchestration
        │   ├── schemas.py              # Pydantic schemas (API contracts)
        │   └── use_cases/               # One class per CRUD action
        │       ├── create.py
        │       ├── retrieve.py
        │       ├── list.py
        │       ├── update.py
        │       └── delete.py
        └── infrastructure/             # External adapters
            ├── models.py               # SQLAlchemy ORM model
            ├── database.py             # Repository implementation
            ├── unit_of_work.py         # SQLAlchemy UoW implementation
            ├── web.py                  # FastAPI routes
            └── exception_handlers.py   # Maps domain exceptions to HTTP responses
```

## Architecture Principles

### Domain Layer (Core)
- Pure business logic
- No external dependencies (no Pydantic, FastAPI, SQLAlchemy in DTOs)
- Defines interfaces (ports) for infrastructure
- Uses simple dataclasses for DTOs

### Application Layer (Use Cases)
- Orchestrates domain logic
- Defines API contracts (Pydantic schemas)
- Maps between layers
- Depends only on Domain layer

### Infrastructure Layer (Adapters)
- Implements domain interfaces
- Handles external concerns (database, web, etc.)
- Depends on Domain and Application layers
- Injects dependencies via FastAPI

## Example: Generated Code

### Domain DTO (Pure Python)
```python
from dataclasses import dataclass

@dataclass
class CreateSchoolDTO:
    name: str
    address: str
    principal_name: str
    student_capacity: int
```

### Domain Model (SQLAlchemy 2.0)
```python
from sqlalchemy.orm import Mapped, mapped_column

class School(Base):
    __tablename__ = "schools"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[str]
    principal_name: Mapped[str]
    student_capacity: Mapped[int]
```

### Application Schema (Pydantic V2)
```python
from pydantic import BaseModel, Field

class CreateSchoolRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: str = Field(..., min_length=1)
    principal_name: str = Field(..., min_length=1)
    student_capacity: int = Field(..., ge=0)
```

### Use Case (Application Layer)

The repository (port) and the `UnitOfWork` (transaction boundary) are injected
separately — both FastAPI dependencies resolve to the same `AsyncSession` per
request, so a `unit_of_work.commit()` after a repository call commits that
call's changes:

```python
class CreateUseCase:
    def __init__(self, *, unit_of_work: UnitOfWork, school_repository: SchoolRepository):
        self.unit_of_work = unit_of_work
        self.school_repository = school_repository

    async def execute(self, *, data: CreateSchoolData) -> School:
        school = await self.school_repository.create(data=data)
        await self.unit_of_work.commit()
        return school
```

## Design Patterns Used

- **Hexagonal Architecture**: Clean separation of concerns
- **Repository Pattern**: Data access abstraction
- **Unit of Work**: Transaction management
- **Dependency Injection**: FastAPI Depends()
- **Mapper Pattern**: Layer-to-layer conversion
- **Factory Pattern**: Generator creation

## Architecture Validation

The generator includes a validator that checks:

- Domain doesn't import Application/Infrastructure
- Application doesn't import Infrastructure
- No SQLAlchemy Session in use cases
- Proper use of DTOs in domain layer
- Dependency inversion respected

```python
from hexagon_generator.utils import ArchitectureValidator
validator = ArchitectureValidator(Path("generated_project"))
result = validator.validate_module("school")
```

## Docker Usage

```bash
# Build image
docker build -f generator.dockerfile -t hexagon-generator:latest .

# Run generator
docker run --name hexagon-generator -p 8069:8069 \
  -v "${PWD}:/mounted_project" \
  hexagon-generator:latest
```

## Project Structure

```
.
├── code_generator.py        # CLI entry point
├── hexagon_generator/       # Core generator
│   ├── core/               # Generation logic
│   ├── templates/          # Jinja2 templates
│   └── utils/              # Validators, path builders
└── generated_project/      # Default output directory
```

### Customizing Templates

Templates are in `hexagon_generator/templates/crud/`. Edit them to customize generated code.

## Documentation

- [Hexagon Generator README](hexagon_generator/readme.md) - Generator details

## Contributing

Contributions welcome! Areas to improve:

- Additional generators (GraphQL, gRPC, etc.)
- Template customization options
- Test generation
- Documentation generation

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

Built with:
- FastAPI
- SQLAlchemy 2.0
- Pydantic V2
- Jinja2
