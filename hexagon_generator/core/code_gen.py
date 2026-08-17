"""Code generation module using Jinja2 templates."""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

from jinja2 import Environment, FileSystemLoader

from hexagon_generator.utils import FileHandler

logger = logging.getLogger(__name__)

# Templates are real .j2 files rendered against the generated Python/FastAPI
# code they produce, which relies heavily on "{}" (dicts, sets, f-strings,
# route paths) and "[]" (generics like list[X]). Jinja's default "{{ }}" and
# alternatives like "[[ ]]" collide with that output, forcing escape hacks.
# "<<" / ">>" and "<%" / "%>" never appear in this generated code, so no
# escaping is needed for the vast majority of templates.
CRUD_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "crud"

_jinja_env = Environment(
    loader=FileSystemLoader(str(CRUD_TEMPLATES_DIR)),
    variable_start_string="<<",
    variable_end_string=">>",
    block_start_string="<%",
    block_end_string="%>",
    comment_start_string="<#",
    comment_end_string="#>",
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)


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

    def render(self, template_name: str, **extra_context: Dict) -> str:
        """
        Render a .j2 template (by name, relative to CRUD_TEMPLATES_DIR) with
        the model context.

        Args:
            template_name: Filename of the template to render
            **extra_context: Additional context variables

        Returns:
            Rendered template as string
        """
        template = _jinja_env.get_template(template_name)

        context = {
            "model_snake_case": self.snake_case,
            "model_pascal_case": self.pascal_case,
            "actions": self.actions,
            **extra_context,
        }

        rendered = template.render(context)
        logger.debug(f"Rendered template {template_name} for {self.pascal_case}")
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

    def render_template(self, *, template_name: str, **extra_context) -> None:
        """
        Render a template and store result.

        Args:
            template_name: Filename of the .j2 template to render
            **extra_context: Additional context variables
        """
        self.template = self.renderer.render(template_name, **extra_context)

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
