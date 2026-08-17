"""Configuration module for hexagon generator."""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass(frozen=True)
class CrudConfig:
    """Configuration for CRUD generator."""

    actions: List[str] = field(
        default_factory=lambda: ["create", "list", "retrieve", "update", "delete"]
    )

    directories: List[str] = field(
        default_factory=lambda: [
            "",
            "application",
            "domain",
            "infrastructure",
            "application/use_cases",
        ]
    )

    def get_routes(self) -> List[Tuple[str, str]]:
        """
        Get list of routes with their corresponding template filenames.

        Templates live as .j2 files in hexagon_generator/templates/crud/ and
        are resolved by TemplateRenderer via a Jinja Environment.

        Returns:
            List of tuples (relative_path, template_name)
        """
        return [
            ("infrastructure/web.py", "infrastructure_web.py.j2"),
            ("infrastructure/database.py", "infrastructure_database.py.j2"),
            ("infrastructure/models.py", "infrastructure_models.py.j2"),
            ("infrastructure/unit_of_work.py", "infrastructure_unit_of_work.py.j2"),
            ("infrastructure/exception_handlers.py", "infrastructure_exception_handlers.py.j2"),
            ("domain/entities.py", "domain_entities.py.j2"),
            ("domain/exceptions.py", "domain_exceptions.py.j2"),
            ("domain/repository.py", "domain_repository.py.j2"),
            ("domain/unit_of_work.py", "domain_unit_of_work.py.j2"),
            ("application/schemas.py", "application_schemas.py.j2"),
        ]

    def get_use_case_templates(self) -> Tuple[str, str]:
        """
        Get use case template filenames.

        Returns:
            Tuple of (init_template_name, individual_use_case_template_name)
        """
        return "application_use_case_init.py.j2", "application_use_case.py.j2"


@dataclass(frozen=True)
class BaseProjectConfig:
    """Configuration for base project structure."""

    mandatory_dirs: List[str] = field(
        default_factory=lambda: [
            "env_vars",
            "src/alembic",
            "src/common",
        ]
    )

    mandatory_files: List[str] = field(
        default_factory=lambda: [
            "src/__init__.py",
            "src/main.py",
            "src/config.py",
            ".env",
            ".gitignore",
            "alembic.ini",
            "docker-compose.yml",
            "dockerfile",
            "init.sh",
            "requirements.txt",
            "readme.md",
        ]
    )


@dataclass(frozen=True)
class BuiltinAppsConfig:
    """Configuration for built-in applications."""

    available_apps: List[str] = field(
        default_factory=lambda: ["user", "role", "auth", "smtp"]
    )

    def is_valid_app(self, app_name: str) -> bool:
        """Check if an app name is valid."""
        return app_name in self.available_apps


# Global configuration instances
CRUD_CONFIG = CrudConfig()
BASE_PROJECT_CONFIG = BaseProjectConfig()
BUILTIN_APPS_CONFIG = BuiltinAppsConfig()
