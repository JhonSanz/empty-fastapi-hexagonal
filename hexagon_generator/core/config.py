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
        Get list of routes with their corresponding templates.

        Returns:
            List of tuples (relative_path, template_content)
        """
        from hexagon_generator.templates.crud.application_handlers import (
            APPLICATION_HANDLERS_TEMPLATE,
        )
        from hexagon_generator.templates.crud.application_interfaces import (
            APPLICATION_INTERFACES_TEMPLATE,
        )
        from hexagon_generator.templates.crud.application_mappers import (
            APPLICATION_MAPPERS_TEMPLATE,
        )
        from hexagon_generator.templates.crud.application_schemas import (
            APPLICATION_SCHEMAS_TEMPLATE,
        )
        from hexagon_generator.templates.crud.application_service import (
            APPLICATION_SERVICE_TEMPLATE,
        )
        from hexagon_generator.templates.crud.domain_dtos import (
            DOMAIN_DTOS_TEMPLATE,
        )
        from hexagon_generator.templates.crud.domain_exceptions import (
            DOMAIN_EXCEPTIONS_TEMPLATE,
        )
        from hexagon_generator.templates.crud.domain_models import (
            DOMAIN_MODELS_TEMPLATE,
        )
        from hexagon_generator.templates.crud.domain_repository import (
            DOMAIN_REPOSITORY_TEMPLATE,
        )
        from hexagon_generator.templates.crud.domain_unit_of_work import (
            DOMAIN_UNIT_OF_WORK_TEMPLATE,
        )
        from hexagon_generator.templates.crud.infrastructure_database import (
            INFRASTRUCTURE_DATABASE_TEMPLATE,
        )
        from hexagon_generator.templates.crud.infrastructure_unit_of_work import (
            INFRASTRUCTURE_UNIT_OF_WORK_TEMPLATE,
        )
        from hexagon_generator.templates.crud.infrastructure_web import (
            INFRASTRUCTURE_WEB_TEMPLATE,
        )

        return [
            ("infrastructure/web.py", INFRASTRUCTURE_WEB_TEMPLATE),
            ("infrastructure/database.py", INFRASTRUCTURE_DATABASE_TEMPLATE),
            ("infrastructure/unit_of_work.py", INFRASTRUCTURE_UNIT_OF_WORK_TEMPLATE),
            ("domain/exceptions.py", DOMAIN_EXCEPTIONS_TEMPLATE),
            ("domain/models.py", DOMAIN_MODELS_TEMPLATE),
            ("domain/repository.py", DOMAIN_REPOSITORY_TEMPLATE),
            ("domain/dtos.py", DOMAIN_DTOS_TEMPLATE),
            ("domain/unit_of_work.py", DOMAIN_UNIT_OF_WORK_TEMPLATE),
            ("application/service.py", APPLICATION_SERVICE_TEMPLATE),
            ("application/schemas.py", APPLICATION_SCHEMAS_TEMPLATE),
            ("application/handlers.py", APPLICATION_HANDLERS_TEMPLATE),
            ("application/mappers.py", APPLICATION_MAPPERS_TEMPLATE),
            ("application/interfaces.py", APPLICATION_INTERFACES_TEMPLATE),
        ]

    def get_use_case_templates(self) -> Tuple[str, str]:
        """
        Get use case templates.

        Returns:
            Tuple of (init_template, individual_use_case_template)
        """
        from hexagon_generator.templates.crud.application_web_cases import (
            APPLICATION_WEB_CASE_TEMPLATE,
            APPLICATION_WEB_CASE_TEMPLATE_INIT,
        )

        return APPLICATION_WEB_CASE_TEMPLATE_INIT, APPLICATION_WEB_CASE_TEMPLATE


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
