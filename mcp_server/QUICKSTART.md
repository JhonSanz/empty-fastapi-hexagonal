# MCP Server Quick Start Guide

Get started with the Hexagonal Generator MCP Server in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- Claude Desktop installed
- Basic understanding of FastAPI and hexagonal architecture

## Step 1: Installation

```bash
# Clone or navigate to the project
cd empty-fastapi-hexagonal

# Install the package with MCP support
pip install -e ".[mcp]"
```

## Step 2: Configure Claude Desktop

1. Locate your Claude Desktop config file:
   - **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the hexagonal-generator MCP server:

```json
{
  "mcpServers": {
    "hexagonal-generator": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/absolute/path/to/empty-fastapi-hexagonal"
    }
  }
}
```

**Important**: Replace `/absolute/path/to/empty-fastapi-hexagonal` with your actual path!

3. Restart Claude Desktop

## Step 3: Verify Installation

Open Claude Desktop and type:

> "Use the hexagonal-generator MCP server to generate a CRUD module for Product"

If configured correctly, Claude will use the MCP server to generate your module.

## Step 4: Your First CRUD Module

### Generate a Module

Chat with Claude:

> "Generate a CRUD module for Book using the hexagonal-generator"

Claude will:
1. Call the `generate_crud` tool
2. Create a complete module structure
3. Report what was generated
4. List TODOs that need completion

### List TODOs

> "Show me all the TODOs in the book module"

Claude will:
1. Scan the generated files
2. Organize TODOs by layer and file type
3. Provide a summary

### Complete TODOs

> "Complete the TODOs in the book domain DTOs. A book has title, author, ISBN, publication year, and page count."

Claude will:
1. Read the file
2. Use specialized prompts for domain DTOs
3. Generate appropriate field definitions
4. Update the file with proper implementations

### Validate Architecture

> "Validate that the book module follows hexagonal architecture"

Claude will:
1. Check dependency rules
2. Scan for violations
3. Calculate compliance score
4. Report any issues

## Complete Example Session

```
You: Generate a CRUD module for Product

Claude: I'll generate a Product CRUD module using the hexagonal-generator.
[Uses generate_crud tool]
✅ Generated 11 files in src/product/
📝 Found 15 TODOs to complete

You: List the TODOs

Claude: Here are the TODOs organized by layer:
[Uses list_todos tool]

Domain Layer (5 TODOs):
- dtos.py: Add your domain fields here
- models.py: Add your SQLAlchemy columns here

Application Layer (6 TODOs):
- schemas.py: Add CreateProductRequest fields
- schemas.py: Add ProductResponse fields
...

You: Complete the domain DTOs. A product has name, description, price, stock quantity, and SKU.

Claude: I'll complete the domain DTOs with those fields.
[Uses complete_todos tool]
✅ Updated src/product/domain/dtos.py with:
- name: str
- description: str
- price: float
- stock_quantity: int
- sku: str

You: Now complete the domain model

Claude: I'll add the SQLAlchemy columns to the Product model.
[Uses complete_todos tool]
✅ Updated src/product/domain/models.py with proper Mapped fields

You: Complete the schemas with validations

Claude: I'll add Pydantic schemas with appropriate validations.
[Uses complete_todos tool]
✅ Added CreateProductRequest with:
- name: min_length=1, max_length=200
- price: ge=0
- stock_quantity: ge=0
- sku: regex pattern for SKU format

You: Validate the architecture

Claude: Let me check architecture compliance.
[Uses validate_hexagonal_architecture tool]
✅ Compliance Score: 100/100
No violations found! The module follows hexagonal architecture principles.
```

## Tips for Success

### 1. Provide Context
When completing TODOs, give Claude context about your domain:

> "Complete the TODOs. A customer has name, email (unique), phone, address, and registration date."

### 2. Work Layer by Layer
Follow the hexagonal flow:
1. Domain DTOs (pure data)
2. Domain Models (SQLAlchemy)
3. Application Schemas (Pydantic with validations)
4. Use Cases (business logic)

### 3. Validate Frequently
Check architecture compliance after completing each layer:

> "Validate the module architecture"

### 4. Iterate
If validation finds issues, ask Claude to fix them:

> "Fix the dependency violations in the customer module"

## Common Issues

### MCP Server Not Found

**Problem**: Claude says it doesn't know about hexagonal-generator

**Solution**:
1. Check config file location
2. Verify absolute path is correct
3. Restart Claude Desktop

### Import Errors

**Problem**: ModuleNotFoundError when running server

**Solution**:
```bash
pip install -e ".[mcp]"
```

### Permission Errors

**Problem**: Cannot write to generated_project/

**Solution**:
- Ensure write permissions in project directory
- Try running from a location you own

## Next Steps

- Read the full [README](README.md) for detailed documentation
- Explore the generated code to understand the structure
- Customize templates in `hexagon_generator/templates/crud/`
- Add your own MCP tools in `mcp_server/tools/`

## Getting Help

- Check the [main documentation](../README.md)
- Review generated code examples
- Look at template files for customization options

Happy coding! 🚀
