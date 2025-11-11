"""Tool to validate hexagonal architecture compliance."""

import ast
import re
from pathlib import Path
from typing import Any


class ArchitectureValidator:
    """Validates that generated code follows hexagonal architecture principles."""

    def __init__(self, project_path: Path):
        """Initialize the validator.

        Args:
            project_path: Path to the FastAPI project
        """
        self.project_path = project_path
        self.src_path = project_path / "src"

        # Define allowed dependencies for each layer
        self.dependency_rules = {
            "domain": {
                "allowed_imports": [
                    "dataclasses",
                    "datetime",
                    "typing",
                    "abc",
                    "enum",
                    "uuid",
                ],
                "forbidden_patterns": [
                    "fastapi",
                    "pydantic",
                    "sqlalchemy",
                    "infrastructure",
                    "application.schemas",
                    "application.handlers",
                ]
            },
            "application": {
                "allowed_imports": [
                    "pydantic",
                    "typing",
                    "datetime",
                    "domain",
                ],
                "forbidden_patterns": [
                    "fastapi",
                    "sqlalchemy.orm.session",
                    "infrastructure.database",
                    "infrastructure.web",
                ]
            },
            "infrastructure": {
                "allowed_imports": [
                    "fastapi",
                    "sqlalchemy",
                    "domain",
                    "application",
                ],
                "forbidden_patterns": []
            }
        }

    def validate_module(self, module_name: str) -> dict[str, Any]:
        """Validate a module's architecture compliance.

        Args:
            module_name: Name of the module (snake_case)

        Returns:
            Validation result with violations and score
        """
        module_path = self.src_path / module_name

        if not module_path.exists():
            return {
                "success": False,
                "error": f"Module not found: {module_path}"
            }

        violations = []

        # Check each layer
        for layer in ["domain", "application", "infrastructure"]:
            layer_path = module_path / layer
            if layer_path.exists():
                layer_violations = self._validate_layer(layer_path, layer, module_name)
                violations.extend(layer_violations)

        # Calculate compliance score
        total_files = sum(1 for _ in module_path.rglob("*.py") if _.name != "__init__.py")
        violation_count = len(violations)

        if total_files == 0:
            score = 0
        else:
            score = max(0, 100 - (violation_count * 10))

        result = {
            "success": True,
            "module": module_name,
            "total_files": total_files,
            "violations_found": violation_count,
            "compliance_score": score,
            "violations": violations,
            "summary": self._generate_summary(violations, score)
        }

        return result

    def _validate_layer(
        self,
        layer_path: Path,
        layer_name: str,
        module_name: str
    ) -> list[dict[str, Any]]:
        """Validate a specific layer.

        Args:
            layer_path: Path to the layer directory
            layer_name: Name of the layer (domain, application, infrastructure)
            module_name: Name of the module

        Returns:
            List of violations found
        """
        violations = []
        rules = self.dependency_rules.get(layer_name, {})

        for python_file in layer_path.glob("*.py"):
            if python_file.name == "__init__.py":
                continue

            file_violations = self._check_file_imports(
                python_file,
                layer_name,
                module_name,
                rules
            )
            violations.extend(file_violations)

        return violations

    def _check_file_imports(
        self,
        file_path: Path,
        layer_name: str,
        module_name: str,
        rules: dict[str, list[str]]
    ) -> list[dict[str, Any]]:
        """Check imports in a file against architecture rules.

        Args:
            file_path: Path to the Python file
            layer_name: Name of the layer
            module_name: Name of the module
            rules: Dependency rules for this layer

        Returns:
            List of violations
        """
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    violation = self._check_import_node(
                        node,
                        file_path,
                        layer_name,
                        module_name,
                        rules
                    )
                    if violation:
                        violations.append(violation)

        except Exception as e:
            violations.append({
                "file": str(file_path.relative_to(self.project_path)),
                "layer": layer_name,
                "type": "parse_error",
                "message": f"Failed to parse file: {str(e)}"
            })

        return violations

    def _check_import_node(
        self,
        node: ast.AST,
        file_path: Path,
        layer_name: str,
        module_name: str,
        rules: dict[str, list[str]]
    ) -> dict[str, Any] | None:
        """Check a single import node.

        Args:
            node: AST import node
            file_path: Path to the file
            layer_name: Name of the layer
            module_name: Name of the module
            rules: Dependency rules

        Returns:
            Violation dictionary if found, None otherwise
        """
        forbidden_patterns = rules.get("forbidden_patterns", [])

        if isinstance(node, ast.Import):
            for alias in node.names:
                for pattern in forbidden_patterns:
                    if pattern in alias.name:
                        return {
                            "file": str(file_path.relative_to(self.project_path)),
                            "layer": layer_name,
                            "type": "forbidden_import",
                            "import": alias.name,
                            "line": node.lineno,
                            "message": f"{layer_name.capitalize()} layer should not import {pattern}"
                        }

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for pattern in forbidden_patterns:
                if pattern in module:
                    return {
                        "file": str(file_path.relative_to(self.project_path)),
                        "layer": layer_name,
                        "type": "forbidden_import",
                        "import": f"from {module}",
                        "line": node.lineno,
                        "message": f"{layer_name.capitalize()} layer should not import from {pattern}"
                    }

        return None

    def _generate_summary(self, violations: list[dict[str, Any]], score: int) -> str:
        """Generate a human-readable summary.

        Args:
            violations: List of violations
            score: Compliance score

        Returns:
            Summary string
        """
        if score >= 90:
            status = "Excellent"
        elif score >= 70:
            status = "Good"
        elif score >= 50:
            status = "Fair"
        else:
            status = "Needs Improvement"

        violation_types = {}
        for v in violations:
            v_type = v.get("type", "unknown")
            violation_types[v_type] = violation_types.get(v_type, 0) + 1

        summary_parts = [
            f"Architecture Compliance: {status} ({score}/100)",
            f"Total Violations: {len(violations)}"
        ]

        if violation_types:
            summary_parts.append("Violation Types:")
            for v_type, count in violation_types.items():
                summary_parts.append(f"  - {v_type}: {count}")

        return "\n".join(summary_parts)
