"""Path building utilities using pathlib."""

from pathlib import Path
from typing import Union


class PathBuilder:
    """
    Helper class for building consistent paths in the hexagon architecture.

    Uses pathlib for safe, cross-platform path manipulation.
    """

    def __init__(self, target_root: Union[str, Path], base_dir: str = ""):
        """
        Initialize PathBuilder.

        Args:
            target_root: Root directory for generated files
            base_dir: Base directory name (usually the module name in snake_case)
        """
        self.target_root = Path(target_root)
        self.base_dir = base_dir

    def get_src_path(self, *parts: str) -> Path:
        """
        Build path under src/ directory.

        Args:
            *parts: Path components to append after src/

        Returns:
            Complete Path object

        Examples:
            >>> pb = PathBuilder("/project", "user")
            >>> pb.get_src_path("application", "service.py")
            Path('/project/src/user/application/service.py')
        """
        return self.target_root / "src" / self.base_dir / Path(*parts) if parts else self.target_root / "src" / self.base_dir

    def get_module_path(self, *parts: str) -> Path:
        """
        Build path under the module directory (src/module_name/).

        Alias for get_src_path for clarity when working with modules.

        Args:
            *parts: Path components

        Returns:
            Complete Path object
        """
        return self.get_src_path(*parts)

    def get_application_path(self, *parts: str) -> Path:
        """
        Build path under application/ layer.

        Args:
            *parts: Path components after application/

        Returns:
            Complete Path object
        """
        return self.get_src_path("application", *parts)

    def get_domain_path(self, *parts: str) -> Path:
        """
        Build path under domain/ layer.

        Args:
            *parts: Path components after domain/

        Returns:
            Complete Path object
        """
        return self.get_src_path("domain", *parts)

    def get_infrastructure_path(self, *parts: str) -> Path:
        """
        Build path under infrastructure/ layer.

        Args:
            *parts: Path components after infrastructure/

        Returns:
            Complete Path object
        """
        return self.get_src_path("infrastructure", *parts)

    def get_use_cases_path(self, *parts: str) -> Path:
        """
        Build path under application/use_cases/.

        Args:
            *parts: Path components after use_cases/

        Returns:
            Complete Path object
        """
        return self.get_application_path("use_cases", *parts)

    def get_use_case_init_path(self) -> Path:
        """Get path for use_cases/__init__.py."""
        return self.get_use_cases_path("__init__.py")

    def get_use_case_file_path(self, action: str) -> Path:
        """
        Get path for a specific use case file.

        Args:
            action: Use case action name (e.g., 'create', 'list')

        Returns:
            Path to the use case file
        """
        return self.get_use_cases_path(f"{action}.py")

    def get_layer_init_path(self, layer: str) -> Path:
        """
        Get __init__.py path for a specific layer.

        Args:
            layer: Layer name ('application', 'domain', or 'infrastructure')

        Returns:
            Path to layer's __init__.py
        """
        return self.get_src_path(layer, "__init__.py")

    @staticmethod
    def ensure_parent_exists(filepath: Path) -> None:
        """
        Ensure parent directories exist for a given file path.

        Args:
            filepath: File path whose parents should be created
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)


class BuiltinPathBuilder:
    """Path builder for built-in applications."""

    def __init__(self, source_root: str = "hexagon_generator/builtin_apps"):
        """
        Initialize BuiltinPathBuilder.

        Args:
            source_root: Root directory for built-in app templates
        """
        self.source_root = Path(source_root)

    def get_source_path(self, relative_path: str) -> Path:
        """
        Get full source path for a built-in component.

        Args:
            relative_path: Relative path from builtin_apps/

        Returns:
            Complete Path object
        """
        return self.source_root / relative_path

    def get_target_path(self, target_root: Union[str, Path], relative_path: str) -> Path:
        """
        Get target path where built-in component should be copied.

        Args:
            target_root: Project root directory
            relative_path: Relative path within project

        Returns:
            Complete Path object
        """
        return Path(target_root) / relative_path
