# Hexagonal Generator MCP Server

MCP (Model Context Protocol) server for generating and completing FastAPI CRUD modules with hexagonal architecture.

## Overview

This MCP server allows LLMs (like Claude) to intelligently generate FastAPI CRUD modules following hexagonal architecture principles and complete TODO comments with contextually appropriate implementations.

## Features

### 1. **generate_crud**
Generate a complete CRUD module with hexagonal architecture:
- Domain layer: Models (SQLAlchemy), DTOs, Repository interface, Unit of Work interface
- Application layer: Schemas (Pydantic), Use Cases, Handlers, Mappers
- Infrastructure layer: Database implementation, Web routes, Unit of Work implementation

### 2. **list_todos**
Scan generated modules for TODO comments and organize them by:
- Architecture layer (domain, application, infrastructure)
- File type (models, dtos, schemas, repository, etc.)
- Provides summary statistics

### 3. **complete_todos**
Intelligently complete TODOs in specific files:
- Analyzes file type and architecture layer
- Uses specialized prompts for different file types
- Respects hexagonal architecture principles
- Considers domain context provided by user

### 4. **validate_hexagonal_architecture**
Validate architecture compliance:
- Check dependency rules (domain shouldn't import application/infrastructure)
- Detect forbidden imports in each layer
- Calculate compliance score
- Provide detailed violation reports

### 5. **suggest_domain_model**
Get suggestions for domain models based on descriptions:
- Analyze entity purpose
- Suggest appropriate fields and types
- Recommend relationships
- Propose business rules

## Installation

1. Install the main hexagon_generator package:
```bash
pip install -e .
```

2. Install MCP server dependencies:
```bash
pip install -r mcp_server/requirements.txt
```

## Configuration

Add the server to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hexagonal-generator": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/empty-fastapi-hexagonal"
    }
  }
}
```

## Usage Examples

### Example 1: Generate a School CRUD Module

**User**: Generate a CRUD module for School

**MCP Call**:
```json
{
  "tool": "generate_crud",
  "arguments": {
    "module_name": "School",
    "project_path": "my_project"
  }
}
```

**Result**: Complete module generated with TODOs in:
- `domain/dtos.py`: Add School-specific fields
- `domain/models.py`: Define School SQLAlchemy model
- `application/schemas.py`: Create Pydantic schemas with validations
- And more...

### Example 2: List TODOs

**User**: Show me what needs to be completed in the School module

**MCP Call**:
```json
{
  "tool": "list_todos",
  "arguments": {
    "module_name": "school",
    "project_path": "my_project"
  }
}
```

**Result**: Organized list of all TODOs with file paths and line numbers

### Example 3: Complete Domain DTOs

**User**: Complete the TODOs in school DTOs. A school has name, address, principal name, and student capacity.

**MCP Call**:
```json
{
  "tool": "complete_todos",
  "arguments": {
    "file_path": "/path/to/my_project/src/school/domain/dtos.py",
    "context": "A school has name, address, principal name, and student capacity"
  }
}
```

**Result**: The LLM receives a specialized prompt with:
- File content
- TODO locations
- Hexagonal architecture rules for domain DTOs
- Context about the school domain
- Instructions to complete with appropriate fields

### Example 4: Validate Architecture

**User**: Check if the school module follows hexagonal architecture

**MCP Call**:
```json
{
  "tool": "validate_hexagonal_architecture",
  "arguments": {
    "module_name": "school",
    "project_path": "my_project"
  }
}
```

**Result**: Compliance report with:
- Score (0-100)
- Violations found (forbidden imports, dependency inversions)
- Recommendations for fixes

## Architecture Principles Enforced

### Domain Layer
- ✅ Pure Python dataclasses for DTOs
- ✅ Abstract repository interfaces
- ✅ No external dependencies (Pydantic, FastAPI, etc.)
- ❌ Cannot import from application or infrastructure layers

### Application Layer
- ✅ Pydantic schemas for API contracts
- ✅ Use cases orchestrating business logic
- ✅ Mappers for layer conversion
- ❌ Cannot import SQLAlchemy Session directly
- ❌ Cannot import infrastructure implementations

### Infrastructure Layer
- ✅ SQLAlchemy implementations
- ✅ FastAPI routes with dependency injection
- ✅ Unit of Work for transaction management
- ✅ Can import from all layers

## File Structure Generated

```
my_project/
└── src/
    └── school/
        ├── domain/
        │   ├── models.py          # SQLAlchemy models
        │   ├── dtos.py            # Domain DTOs (dataclasses)
        │   ├── repository.py      # Repository interface
        │   └── unit_of_work.py    # UoW interface
        ├── application/
        │   ├── schemas.py         # Pydantic schemas
        │   ├── handlers.py        # Request handlers
        │   ├── web_cases.py       # Use cases
        │   └── mappers.py         # Layer mappers
        └── infrastructure/
            ├── database.py        # Repository implementation
            ├── web.py             # FastAPI routes
            └── unit_of_work.py    # UoW implementation
```

## TODO Completion Workflow

1. **Generate module**: Creates skeleton with TODOs
2. **List TODOs**: See what needs completion
3. **Complete by layer**:
   - Start with domain DTOs (define data structure)
   - Then domain models (add SQLAlchemy columns)
   - Then schemas (add Pydantic validations)
   - Finally use cases (add business logic)
4. **Validate**: Check architecture compliance
5. **Iterate**: Refine based on validation feedback

## Specialized Prompts

The server provides context-aware prompts for each file type:

- **Domain DTOs**: Focus on pure data structures, no dependencies
- **Domain Models**: SQLAlchemy 2.0 best practices, Mapped types
- **Schemas**: Pydantic V2, Field validations, examples
- **Repository**: select() statements, DTO handling
- **Use Cases**: Business logic, Unit of Work, error handling

## Development

### Running Tests
```bash
pytest mcp_server/tests/
```

### Extending the Server

To add a new tool:

1. Add tool definition in `server.py` `list_tools()`
2. Create handler function `handle_new_tool()`
3. Add to `call_tool()` dispatcher
4. (Optional) Create specialized prompt in `prompts/completion_prompts.py`

## Troubleshooting

### Import errors
Make sure the main package is installed: `pip install -e .`

### MCP server not appearing in Claude
- Check configuration file path
- Verify Python path in config
- Restart Claude Desktop

### Generation fails
- Ensure jinja2 is installed
- Check project_path exists
- Verify write permissions

## License

Same as the parent hexagon_generator project.
