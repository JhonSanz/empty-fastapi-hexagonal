"""Built-in application generator for copying template apps."""

import logging
from pathlib import Path
from typing import Union

from hexagon_generator.utils import BuiltinPathBuilder, FileHandler

logger = logging.getLogger(__name__)


class BuiltInGenerator:
    """
    Handles copying of built-in application templates.

    Provides methods to copy complete applications or individual files
    from the built-in templates directory.
    """

    def __init__(self, source_root: str = "hexagon_generator/builtin_apps"):
        """
        Initialize BuiltInGenerator.

        Args:
            source_root: Root directory for built-in app templates
        """
        self.path_builder = BuiltinPathBuilder(source_root)
        self.file_handler = FileHandler()

    def copy_builtin_apps(
        self,
        *,
        path_source: str,
        path_target: Union[str, Path],
        overwrite: bool = False,
    ) -> bool:
        """
        Copy a built-in application directory.

        Args:
            path_source: Relative path from builtin_apps/ (e.g., 'src/user')
            path_target: Target path where to copy the directory
            overwrite: If True, overwrite existing directory

        Returns:
            True if directory was copied, False if skipped

        Examples:
            >>> gen = BuiltInGenerator()
            >>> gen.copy_builtin_apps(
            ...     path_source="src/user",
            ...     path_target="/project/src/user"
            ... )
        """
        source = self.path_builder.get_source_path(path_source)
        target = Path(path_target)

        logger.info(f"Copying built-in app from {source} to {target}")

        try:
            return self.file_handler.copy_directory(
                source=source,
                destination=target,
                overwrite=overwrite,
            )
        except Exception as e:
            logger.error(f"Failed to copy built-in app: {e}")
            return False

    def copy_builtin_files(
        self,
        *,
        path_source: str,
        path_target: Union[str, Path],
        overwrite: bool = False,
    ) -> bool:
        """
        Copy a built-in file.

        Args:
            path_source: Relative path from builtin_apps/ (e.g., 'src/main.py')
            path_target: Target path where to copy the file
            overwrite: If True, overwrite existing file

        Returns:
            True if file was copied, False if skipped

        Examples:
            >>> gen = BuiltInGenerator()
            >>> gen.copy_builtin_files(
            ...     path_source="src/main.py",
            ...     path_target="/project/src/main.py"
            ... )
        """
        source = self.path_builder.get_source_path(path_source)
        target = Path(path_target)

        logger.info(f"Copying built-in file from {source} to {target}")

        try:
            return self.file_handler.copy_file(
                source=source,
                destination=target,
                overwrite=overwrite,
            )
        except Exception as e:
            logger.error(f"Failed to copy built-in file: {e}")
            return False
