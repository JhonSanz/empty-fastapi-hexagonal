"""Tool to scan for TODO comments in generated code."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class TodoItem:
    """Represents a TODO comment found in code."""
    file_path: str
    line_number: int
    content: str
    category: str  # domain, application, infrastructure
    file_type: str  # models, dtos, schemas, repository, etc.


class TodoScanner:
    """Scans generated modules for TODO comments."""

    def __init__(self, project_path: Path):
        """Initialize the scanner.

        Args:
            project_path: Path to the FastAPI project
        """
        self.project_path = project_path
        self.src_path = project_path / "src"

    def scan_module(self, module_name: str) -> list[dict[str, Any]]:
        """Scan a module for all TODO comments.

        Args:
            module_name: Name of the module (snake_case)

        Returns:
            List of TODO items with metadata
        """
        module_path = self.src_path / module_name

        if not module_path.exists():
            raise FileNotFoundError(f"Module not found: {module_path}")

        todos: list[TodoItem] = []

        # Scan all Python files in the module
        for python_file in module_path.rglob("*.py"):
            if python_file.name == "__init__.py":
                continue

            todos.extend(self._scan_file(python_file, module_name))

        # Convert to dict format for JSON serialization
        return [self._todo_to_dict(todo) for todo in todos]

    def _scan_file(self, file_path: Path, module_name: str) -> list[TodoItem]:
        """Scan a single file for TODOs.

        Args:
            file_path: Path to the Python file
            module_name: Name of the module

        Returns:
            List of TodoItem objects
        """
        todos: list[TodoItem] = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return todos

        # Pattern to match TODO comments
        todo_pattern = re.compile(r'#\s*TODO:?\s*(.+)', re.IGNORECASE)

        for line_num, line in enumerate(lines, start=1):
            match = todo_pattern.search(line)
            if match:
                todo_content = match.group(1).strip()
                category = self._determine_category(file_path)
                file_type = self._determine_file_type(file_path)

                todos.append(TodoItem(
                    file_path=str(file_path.relative_to(self.project_path)),
                    line_number=line_num,
                    content=todo_content,
                    category=category,
                    file_type=file_type
                ))

        return todos

    def _determine_category(self, file_path: Path) -> str:
        """Determine the architecture layer category.

        Args:
            file_path: Path to the file

        Returns:
            Category name (domain, application, infrastructure)
        """
        parts = file_path.parts
        if "domain" in parts:
            return "domain"
        elif "application" in parts:
            return "application"
        elif "infrastructure" in parts:
            return "infrastructure"
        return "unknown"

    def _determine_file_type(self, file_path: Path) -> str:
        """Determine the specific file type.

        Args:
            file_path: Path to the file

        Returns:
            File type (models, dtos, schemas, repository, etc.)
        """
        return file_path.stem  # Returns filename without extension

    def _todo_to_dict(self, todo: TodoItem) -> dict[str, Any]:
        """Convert TodoItem to dictionary.

        Args:
            todo: TodoItem instance

        Returns:
            Dictionary representation
        """
        return {
            "file_path": todo.file_path,
            "line_number": todo.line_number,
            "content": todo.content,
            "category": todo.category,
            "file_type": todo.file_type
        }

    def get_summary(self, todos: list[dict[str, Any]]) -> dict[str, Any]:
        """Get a summary of TODOs by category and file type.

        Args:
            todos: List of TODO dictionaries

        Returns:
            Summary statistics
        """
        summary = {
            "by_category": {},
            "by_file_type": {},
            "total": len(todos)
        }

        for todo in todos:
            # Count by category
            category = todo["category"]
            summary["by_category"][category] = summary["by_category"].get(category, 0) + 1

            # Count by file type
            file_type = todo["file_type"]
            summary["by_file_type"][file_type] = summary["by_file_type"].get(file_type, 0) + 1

        return summary
