"""Main MCP Server implementation for hexagonal architecture generator."""

import json
import logging
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from hexagon_generator.core.generator_factory import GeneratorFactory
from hexagon_generator.core.config import CrudConfig
from hexagon_generator.utils.validators import normalize_name

from .tools.todo_scanner import TodoScanner
from .tools.todo_completer import TodoCompleter
from .tools.architecture_validator import ArchitectureValidator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
app = Server("hexagonal-generator")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="generate_crud",
            description=(
                "Generate a complete CRUD module following hexagonal architecture. "
                "Creates domain models, DTOs, repositories, use cases, schemas, and API routes. "
                "The generated code includes TODO comments for domain-specific logic that needs completion."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {
                        "type": "string",
                        "description": "Name of the module in PascalCase or snake_case (e.g., 'School' or 'school')"
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Path to the FastAPI project where code will be generated (default: 'generated_project')"
                    }
                },
                "required": ["module_name"]
            }
        ),
        Tool(
            name="list_todos",
            description=(
                "Scan a generated module for TODO comments and return them organized by file and category. "
                "Helps identify what needs to be completed in the generated code."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {
                        "type": "string",
                        "description": "Name of the module to scan (e.g., 'school')"
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Path to the FastAPI project (default: 'generated_project')"
                    }
                },
                "required": ["module_name"]
            }
        ),
        Tool(
            name="complete_todos",
            description=(
                "Intelligently complete TODO comments in a specific file while respecting hexagonal architecture principles. "
                "Analyzes context and generates appropriate domain logic, validations, or business rules."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the file containing TODOs to complete"
                    },
                    "context": {
                        "type": "string",
                        "description": "Additional context about the domain (e.g., 'A school has name, address, and manages students')"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="validate_hexagonal_architecture",
            description=(
                "Validate that a generated module follows hexagonal architecture principles. "
                "Checks for dependency violations, proper layer separation, and architecture compliance."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {
                        "type": "string",
                        "description": "Name of the module to validate (e.g., 'school')"
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Path to the FastAPI project (default: 'generated_project')"
                    }
                },
                "required": ["module_name"]
            }
        ),
        Tool(
            name="suggest_domain_model",
            description=(
                "Suggest domain model fields and relationships based on a description. "
                "Helps design the domain layer following DDD principles."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_name": {
                        "type": "string",
                        "description": "Name of the entity (e.g., 'School', 'Student')"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of what the entity represents and its purpose"
                    }
                },
                "required": ["entity_name", "description"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "generate_crud":
            return await handle_generate_crud(arguments)
        elif name == "list_todos":
            return await handle_list_todos(arguments)
        elif name == "complete_todos":
            return await handle_complete_todos(arguments)
        elif name == "validate_hexagonal_architecture":
            return await handle_validate_architecture(arguments)
        elif name == "suggest_domain_model":
            return await handle_suggest_domain_model(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_generate_crud(arguments: dict[str, Any]) -> list[TextContent]:
    """Generate CRUD module using the hexagonal generator."""
    module_name = arguments["module_name"]
    project_path = arguments.get("project_path", "generated_project")

    try:
        # Normalize the module name
        pascal_name, snake_name = normalize_name(module_name)

        # Create configuration
        config = CrudConfig(
            module_name=pascal_name,
            project_path=Path(project_path)
        )

        # Generate the CRUD module
        generator = GeneratorFactory.create_crud_generator(config)
        generator.generate()

        # Scan for TODOs immediately after generation
        scanner = TodoScanner(Path(project_path))
        todos = scanner.scan_module(snake_name)

        result = {
            "success": True,
            "module": snake_name,
            "pascal_name": pascal_name,
            "project_path": project_path,
            "message": f"CRUD module '{pascal_name}' generated successfully",
            "files_created": [
                f"src/{snake_name}/domain/models.py",
                f"src/{snake_name}/domain/dtos.py",
                f"src/{snake_name}/domain/repository.py",
                f"src/{snake_name}/domain/unit_of_work.py",
                f"src/{snake_name}/application/schemas.py",
                f"src/{snake_name}/application/handlers.py",
                f"src/{snake_name}/application/web_cases.py",
                f"src/{snake_name}/application/mappers.py",
                f"src/{snake_name}/infrastructure/database.py",
                f"src/{snake_name}/infrastructure/web.py",
                f"src/{snake_name}/infrastructure/unit_of_work.py",
            ],
            "todos_found": len(todos),
            "todos": todos
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except Exception as e:
        logger.error(f"Error generating CRUD: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({"success": False, "error": str(e)}, indent=2)
        )]


async def handle_list_todos(arguments: dict[str, Any]) -> list[TextContent]:
    """List all TODOs in a module."""
    module_name = arguments["module_name"]
    project_path = arguments.get("project_path", "generated_project")

    try:
        scanner = TodoScanner(Path(project_path))
        todos = scanner.scan_module(module_name)

        result = {
            "success": True,
            "module": module_name,
            "total_todos": len(todos),
            "todos": todos,
            "summary": scanner.get_summary(todos)
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except Exception as e:
        logger.error(f"Error listing TODOs: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({"success": False, "error": str(e)}, indent=2)
        )]


async def handle_complete_todos(arguments: dict[str, Any]) -> list[TextContent]:
    """Complete TODOs in a specific file."""
    file_path = Path(arguments["file_path"])
    context = arguments.get("context", "")

    try:
        completer = TodoCompleter()
        result = await completer.complete_file_todos(file_path, context)

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except Exception as e:
        logger.error(f"Error completing TODOs: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({"success": False, "error": str(e)}, indent=2)
        )]


async def handle_validate_architecture(arguments: dict[str, Any]) -> list[TextContent]:
    """Validate hexagonal architecture compliance."""
    module_name = arguments["module_name"]
    project_path = arguments.get("project_path", "generated_project")

    try:
        validator = ArchitectureValidator(Path(project_path))
        result = validator.validate_module(module_name)

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except Exception as e:
        logger.error(f"Error validating architecture: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({"success": False, "error": str(e)}, indent=2)
        )]


async def handle_suggest_domain_model(arguments: dict[str, Any]) -> list[TextContent]:
    """Suggest domain model based on description."""
    entity_name = arguments["entity_name"]
    description = arguments["description"]

    try:
        # This will use the LLM's natural capabilities to suggest a model
        # The actual suggestion generation is done by the LLM client
        result = {
            "success": True,
            "entity_name": entity_name,
            "description": description,
            "suggestion": (
                f"Based on the description, I suggest the following structure for {entity_name}:\n\n"
                "Please provide your domain model suggestion including:\n"
                "1. Fields with appropriate types\n"
                "2. Validations and constraints\n"
                "3. Relationships with other entities\n"
                "4. Business rules that should be enforced\n\n"
                f"Context: {description}"
            )
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except Exception as e:
        logger.error(f"Error suggesting domain model: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({"success": False, "error": str(e)}, indent=2)
        )]


async def start_server():
    """Start the MCP server."""
    logger.info("Starting Hexagonal Generator MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    """Entry point for the server."""
    import asyncio
    asyncio.run(start_server())


if __name__ == "__main__":
    main()
