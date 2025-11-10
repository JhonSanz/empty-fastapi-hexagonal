"""Model generator for creating hexagonal architecture modules."""

import logging
from typing import List, Tuple

from jinja2 import Template

from hexagon_generator.core.code_gen import CodeGenerator
from hexagon_generator.core.constant import TARGET_ROOT
from hexagon_generator.utils import PathBuilder

logger = logging.getLogger(__name__)


class ModelGenerator:
    """
    Generates a complete hexagonal architecture module for a model.

    Creates all necessary directories, files, and use cases for CRUD operations.
    """

    def __init__(
        self,
        *,
        pascal_case: str,
        snake_case: str,
        routes: List[Tuple[str, str]],
        dirs: List[str],
        actions: List[str],
        use_cases_init: str,
        use_cases: str,
        code_generator: CodeGenerator,
    ):
        """
        Initialize ModelGenerator.

        Args:
            pascal_case: Model name in PascalCase
            snake_case: Model name in snake_case
            routes: List of (relative_path, template) tuples
            dirs: List of directories to create
            actions: List of CRUD actions to generate
            use_cases_init: Template for use_cases/__init__.py
            use_cases: Template for individual use case files
            code_generator: CodeGenerator instance
        """
        self.pascal_case = pascal_case
        self.snake_case = snake_case
        self.routes = routes
        self.dirs = dirs
        self.actions = actions
        self.use_cases_init = use_cases_init
        self.use_cases = use_cases
        self.code_generator = code_generator
        self.base_dir = pascal_case.lower()

        # Initialize path builder for this module
        self.path_builder = PathBuilder(TARGET_ROOT, self.base_dir)

    def create_mandatory_dirs(self) -> None:
        """Create all mandatory directories for the module."""
        logger.info(f"Creating directories for module: {self.base_dir}")

        for dir_ in self.dirs:
            # Create directory
            dir_path = self.path_builder.get_module_path(dir_)
            self.code_generator.create_dir(dir_name=dir_path)

            # Create __init__.py for each directory except use_cases (handled separately)
            if dir_ != "application/use_cases":
                self._create_init_file(dir_)

    def _create_init_file(self, directory: str) -> None:
        """
        Create an empty __init__.py file in a directory.

        Args:
            directory: Relative directory path
        """
        init_path = self.path_builder.get_module_path(directory, "__init__.py")
        self.code_generator.filepath = init_path
        self.code_generator.template = ""
        self.code_generator.save_file_to_path()

    def create_use_cases(self) -> None:
        """Create all use case files."""
        logger.info(f"Creating use cases for {self.base_dir}")

        self._create_use_cases_init()
        self._create_individual_use_cases()

    def _create_use_cases_init(self) -> None:
        """Create the use_cases/__init__.py file."""
        init_path = self.path_builder.get_use_case_init_path()
        self.code_generator.filepath = init_path
        self.code_generator.render_template(template_imported=self.use_cases_init)
        self.code_generator.save_file_to_path()

    def _create_individual_use_cases(self) -> None:
        """Create individual use case files for each action."""
        template = Template(self.use_cases)

        for action in self.actions:
            self._create_use_case_for_action(action, template)

    def _create_use_case_for_action(self, action: str, template: Template) -> None:
        """
        Create a use case file for a specific action.

        Args:
            action: The action name (e.g., 'create', 'list')
            template: Jinja2 template for rendering
        """
        # Render template for this specific action
        rendered = template.render(
            model_snake_case=self.snake_case,
            model_pascal_case=self.pascal_case,
            action=action,
        )

        # Save to file
        filepath = self.path_builder.get_use_case_file_path(action)
        self.code_generator.filepath = filepath
        self.code_generator.render_template(template_imported=rendered)
        self.code_generator.save_file_to_path()

    def create_routes(self) -> None:
        """Create all route/layer files from templates."""
        logger.info(f"Creating routes/layers for {self.base_dir}")

        for relative_path, template_content in self.routes:
            self._create_route_file(relative_path, template_content)

    def _create_route_file(self, relative_path: str, template_content: str) -> None:
        """
        Create a single route/layer file.

        Args:
            relative_path: Relative path within the module
            template_content: Template content to render
        """
        filepath = self.path_builder.get_module_path(relative_path)
        self.code_generator.filepath = filepath
        self.code_generator.render_template(template_imported=template_content)
        self.code_generator.save_file_to_path()

    def run(self) -> None:
        """
        Run the complete model generation process.

        Creates directories, routes, and use cases for the model.
        """
        logger.info(f"Starting model generation for: {self.pascal_case}")

        self.create_mandatory_dirs()
        self.create_routes()
        self.create_use_cases()

        logger.info(f"Model generation completed for: {self.pascal_case}")
