# Hexagonal Architecture Generator for FastAPI

Generate FastAPI CRUD modules following hexagonal (ports & adapters) architecture principles with AI-powered TODO completion via MCP.

## 🌟 Features

- **Complete CRUD Generation**: Generate domain models, DTOs, repositories, use cases, schemas, and API routes
- **Hexagonal Architecture**: Enforces proper layer separation (Domain, Application, Infrastructure)
- **SQLAlchemy 2.0**: Uses modern Mapped types and select() statements
- **Pydantic V2**: Includes Field validations and OpenAPI documentation
- **Unit of Work Pattern**: Transaction management abstraction
- **MCP Server**: AI-powered TODO completion with Claude Desktop
- **Architecture Validation**: Check compliance with hexagonal principles

## 🚀 Quick Start

### Installation

```bash
# Basic installation
pip install -e .

# With MCP server support
pip install -e ".[mcp]"
```

### CLI Usage

```bash
# Generate a CRUD module
hexagonal-gen crud School

# Specify custom output directory
hexagonal-gen crud Product --output my_project
```

### MCP Server Usage

1. Configure Claude Desktop (see [MCP Server Quick Start](mcp_server/QUICKSTART.md))
2. Chat with Claude: "Generate a CRUD module for Product using hexagonal-generator"
3. Claude will generate the module and help complete TODOs contextually

## 📁 Generated Structure

```
generated_project/
└── src/
    └── school/
        ├── domain/              # Business logic & entities
        │   ├── models.py        # SQLAlchemy ORM models
        │   ├── dtos.py          # Domain data transfer objects
        │   ├── repository.py    # Repository interface (port)
        │   └── unit_of_work.py  # Transaction interface
        ├── application/         # Use cases & orchestration
        │   ├── schemas.py       # Pydantic schemas (API contracts)
        │   ├── handlers.py      # Request handlers
        │   ├── web_cases.py     # Use case implementations
        │   └── mappers.py       # Layer-to-layer mappers
        └── infrastructure/      # External adapters
            ├── database.py      # Repository implementation
            ├── web.py           # FastAPI routes
            └── unit_of_work.py  # SQLAlchemy UoW implementation
```

## 🏗️ Architecture Principles

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

## 🤖 MCP Server

The MCP (Model Context Protocol) server allows Claude to intelligently complete generated code.

### Available Tools

1. **generate_crud**: Generate complete CRUD modules
2. **list_todos**: Scan for TODO comments
3. **complete_todos**: AI-powered TODO completion
4. **validate_hexagonal_architecture**: Check compliance
5. **suggest_domain_model**: Get domain design suggestions

### Example Workflow

```
1. Generate: "Create a CRUD for Product"
2. List: "Show TODOs in product module"
3. Complete: "Complete domain DTOs - product has name, price, SKU"
4. Validate: "Check product architecture compliance"
```

See [MCP Server Documentation](mcp_server/README.md) and [Quick Start](mcp_server/QUICKSTART.md) for details.

## 📝 Example: Generated Code

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
```python
def create_school(
    request: CreateSchoolRequest,
    unit_of_work: UnitOfWork
) -> SchoolResponse:
    dto = SchoolMapper.to_create_dto(request)
    school = unit_of_work.schools.create(dto)
    unit_of_work.commit()
    return SchoolMapper.to_response(school)
```

## 🎯 Design Patterns Used

- **Hexagonal Architecture**: Clean separation of concerns
- **Repository Pattern**: Data access abstraction
- **Unit of Work**: Transaction management
- **Dependency Injection**: FastAPI Depends()
- **Mapper Pattern**: Layer-to-layer conversion
- **Factory Pattern**: Generator creation

## 🔍 Architecture Validation

The generator includes a validator that checks:

✅ Domain doesn't import Application/Infrastructure
✅ Application doesn't import Infrastructure
✅ No SQLAlchemy Session in use cases
✅ Proper use of DTOs in domain layer
✅ Dependency inversion respected

```bash
# Via MCP
"Validate the school module architecture"

# Programmatically
from mcp_server.tools import ArchitectureValidator
validator = ArchitectureValidator(Path("generated_project"))
result = validator.validate_module("school")
```

## 🐳 Docker Usage

```bash
# Build image
docker build -f generator.dockerfile -t hexagon-generator:latest .

# Run generator
docker run --name hexagon-generator -p 8069:8069 \
  -v "${PWD}:/mounted_project" \
  hexagon-generator:latest
```

## 🛠️ Development

### Project Structure

```
.
├── hexagon_generator/       # Core generator
│   ├── core/               # Generation logic
│   ├── templates/          # Jinja2 templates
│   └── utils/              # Validators, path builders
├── mcp_server/             # MCP server implementation
│   ├── tools/              # MCP tools
│   ├── prompts/            # Completion prompts
│   └── server.py           # Main server
└── generated_project/      # Default output directory
```

### Running Tests

```bash
pytest tests/
```

### Customizing Templates

Templates are in `hexagon_generator/templates/crud/`. Edit them to customize generated code.

## 📚 Documentation

- [MCP Server README](mcp_server/README.md) - Detailed MCP documentation
- [MCP Quick Start](mcp_server/QUICKSTART.md) - Get started in 5 minutes
- [Hexagon Generator README](hexagon_generator/readme.md) - Generator details

## 🤝 Contributing

Contributions welcome! Areas to improve:

- Additional generators (GraphQL, gRPC, etc.)
- More MCP tools
- Template customization options
- Test generation
- Documentation generation

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Built with:
- FastAPI
- SQLAlchemy 2.0
- Pydantic V2
- Jinja2
- Model Context Protocol (MCP)