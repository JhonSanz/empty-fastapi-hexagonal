"""Base directory and file generator for project initialization."""

import logging
from pathlib import Path

from hexagon_generator.core.builtin_gen import BuiltInGenerator
from hexagon_generator.core.config import BASE_PROJECT_CONFIG
from hexagon_generator.core.constant import TARGET_ROOT

logger = logging.getLogger(__name__)


class BaseDirsGenerator:
    """
    Generates base project structure.

    Creates mandatory directories and files for a new hexagonal FastAPI project.
    """

    def __init__(self, builtin_gen: BuiltInGenerator):
        """
        Initialize BaseDirsGenerator.

        Args:
            builtin_gen: BuiltInGenerator instance for copying templates
        """
        self.builtin_gen = builtin_gen
        self.config = BASE_PROJECT_CONFIG
        self.target_root = Path(TARGET_ROOT)

    def create_mandatory_dirs(self) -> None:
        """Create all mandatory directories from configuration."""
        logger.info("Creating mandatory directories")

        for path in self.config.mandatory_dirs:
            target = self.target_root / path
            self.builtin_gen.copy_builtin_apps(
                path_source=path,
                path_target=target,
            )

    def create_mandatory_files(self) -> None:
        """Create all mandatory files from configuration."""
        logger.info("Creating mandatory files")

        for path in self.config.mandatory_files:
            target = self.target_root / path
            self.builtin_gen.copy_builtin_files(
                path_source=path,
                path_target=target,
            )

    def run(self) -> None:
        """
        Run the complete base structure generation process.

        Creates all mandatory directories and files.
        """
        logger.info("Starting base project structure generation")

        self.create_mandatory_dirs()
        self.create_mandatory_files()

        logger.info("Base directories and files created successfully")
