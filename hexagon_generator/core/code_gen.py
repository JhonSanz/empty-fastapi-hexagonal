"""Code generation module using Jinja2 templates."""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

from jinja2 import Template

from hexagon_generator.utils import FileHandler

logger = logging.getLogger(__name__)


class TemplateRenderer:
    """
    Handles template rendering using Jinja2.

    Separated from file operations for better testability and single responsibility.
    """

    def __init__(
        self,
        *,
        pascal_case: str,
        snake_case: str,
        actions: Optional[List[str]] = None,
    ):
        """
        Initialize TemplateRenderer.

        Args:
            pascal_case: Model name in PascalCase
            snake_case: Model name in snake_case
            actions: List of HTTP actions to generate
        """
        self.pascal_case = pascal_case
        self.snake_case = snake_case
        self.actions = actions or []

    def render(self, template_content: str, **extra_context: Dict) -> str:
        """
        Render a template with the model context.

        Args:
            template_content: Template string to render
            **extra_context: Additional context variables

        Returns:
            Rendered template as string
        """
        template = Template(template_content)

        context = {
            "model_snake_case": self.snake_case,
            "model_pascal_case": self.pascal_case,
            "actions": self.actions,
            **extra_context,
        }

        rendered = template.render(context)
        logger.debug(f"Rendered template for {self.pascal_case}")
        return rendered


class CodeGenerator:
    """
    Main code generator class.

    Combines template rendering with file operations.
    Maintains backward compatibility while using new utilities.
    """

    def __init__(
        self,
        *,
        pascal_case: str,
        snake_case: str,
        HTTP_ACTIONS: Optional[List[str]] = None,
        filepath: Optional[Union[str, Path]] = None,
    ):
        """
        Initialize CodeGenerator.

        Args:
            pascal_case: Model name in PascalCase
            snake_case: Model name in snake_case
            HTTP_ACTIONS: List of HTTP actions (kept for backward compatibility)
            filepath: Optional file path for backward compatibility
        """
        self.pascal_case = pascal_case
        self.snake_case = snake_case
        self.HTTP_ACTIONS = HTTP_ACTIONS or []
        self.filepath = filepath
        self.template: Optional[str] = None

        self.renderer = TemplateRenderer(
            pascal_case=pascal_case,
            snake_case=snake_case,
            actions=self.HTTP_ACTIONS,
        )
        self.file_handler = FileHandler()

    def render_template(self, *, template_imported: str, **extra_context) -> None:
        """
        Render a template and store result.

        Args:
            template_imported: Template string to render
            **extra_context: Additional context variables
        """
        self.template = self.renderer.render(template_imported, **extra_context)

    def save_file_to_path(self, overwrite: bool = False) -> bool:
        """
        Save rendered template to file.

        Args:
            overwrite: If True, overwrite existing file

        Returns:
            True if file was saved, False if skipped
        """
        if not self.filepath:
            logger.error("No filepath set")
            return False

        if self.template is None:
            logger.error("No template rendered")
            return False

        return self.file_handler.write_file(
            filepath=self.filepath,
            content=self.template,
            overwrite=overwrite,
        )

    @staticmethod
    def create_dir(*, dir_name: Union[str, Path]) -> bool:
        """
        Create a directory.

        Static method for backward compatibility.

        Args:
            dir_name: Directory path to create

        Returns:
            True if directory was created, False if already existed
        """
        return FileHandler.create_directory(dir_name)
