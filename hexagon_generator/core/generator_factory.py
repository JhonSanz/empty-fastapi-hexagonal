"""Factory for creating different types of generators."""

import logging
from typing import Optional

from hexagon_generator.core.base_check_gen import BaseDirsGenerator
from hexagon_generator.core.builtin_gen import BuiltInGenerator
from hexagon_generator.core.code_gen import CodeGenerator
from hexagon_generator.core.config import BUILTIN_APPS_CONFIG, CRUD_CONFIG
from hexagon_generator.core.constant import TARGET_ROOT
from hexagon_generator.core.model_gen import ModelGenerator
from hexagon_generator.utils import NamingError, normalize_name

logger = logging.getLogger(__name__)


class GeneratorType:
    """Constants for generator types."""
    CRUD = "crud"
    BUILTIN = "builtin"


class GeneratorFactory:
    """
    Factory for creating generator instances.

    Provides a clean interface for creating different types of generators
    without exposing implementation details.
    """

    @staticmethod
    def create_crud_generator(
        model_name: str,
        actions: Optional[list[str]] = None,
    ) -> ModelGenerator:
        """
        Create a CRUD model generator.

        Args:
            model_name: Model name (can be PascalCase or snake_case)
            actions: Optional list of CRUD actions (defaults to all)

        Returns:
            Configured ModelGenerator instance

        Raises:
            NamingError: If model_name is invalid

        Examples:
            >>> factory = GeneratorFactory()
            >>> gen = factory.create_crud_generator("UserAccount")
            >>> gen.run()
        """
        # Normalize the name
        try:
            pascal_case, snake_case = normalize_name(model_name)
        except NamingError as e:
            logger.error(f"Invalid model name: {e}")
            raise

        logger.info(f"Creating CRUD generator for {pascal_case} ({snake_case})")

        # Use config defaults if actions not provided
        if actions is None:
            actions = CRUD_CONFIG.actions

        # Create code generator
        code_generator = CodeGenerator(
            pascal_case=pascal_case,
            snake_case=snake_case,
            HTTP_ACTIONS=actions,
        )

        # Get templates from config
        routes = CRUD_CONFIG.get_routes()
        use_cases_init, use_cases = CRUD_CONFIG.get_use_case_templates()

        # Create and return model generator
        return ModelGenerator(
            pascal_case=pascal_case,
            snake_case=snake_case,
            dirs=CRUD_CONFIG.directories,
            routes=routes,
            actions=actions,
            use_cases_init=use_cases_init,
            use_cases=use_cases,
            code_generator=code_generator,
        )

    @staticmethod
    def create_builtin_generator(app_name: str) -> tuple[BuiltInGenerator, str, str]:
        """
        Create a built-in app generator.

        Args:
            app_name: Name of the built-in app (e.g., 'user', 'auth')

        Returns:
            Tuple of (generator, source_path, target_path)

        Raises:
            ValueError: If app_name is not a valid built-in app

        Examples:
            >>> factory = GeneratorFactory()
            >>> gen, src, tgt = factory.create_builtin_generator("user")
            >>> gen.copy_builtin_apps(path_source=src, path_target=tgt)
        """
        if not BUILTIN_APPS_CONFIG.is_valid_app(app_name):
            available = ", ".join(BUILTIN_APPS_CONFIG.available_apps)
            error_msg = (
                f"Invalid built-in app: '{app_name}'. "
                f"Available apps: {available}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Creating built-in generator for {app_name}")

        generator = BuiltInGenerator()
        source_path = f"src/{app_name}"
        target_path = f"{TARGET_ROOT}/src/{app_name}"

        return generator, source_path, target_path

    @staticmethod
    def create_base_generator() -> BaseDirsGenerator:
        """
        Create a base project structure generator.

        Returns:
            Configured BaseDirsGenerator instance

        Examples:
            >>> factory = GeneratorFactory()
            >>> gen = factory.create_base_generator()
            >>> gen.run()
        """
        logger.info("Creating base project generator")

        builtin_gen = BuiltInGenerator()
        return BaseDirsGenerator(builtin_gen=builtin_gen)

    @staticmethod
    def create_from_type(
        generator_type: str,
        **kwargs,
    ):
        """
        Create a generator based on type string.

        Args:
            generator_type: Type of generator ('crud' or 'builtin')
            **kwargs: Additional arguments for the specific generator

        Returns:
            Appropriate generator instance

        Raises:
            ValueError: If generator_type is unknown

        Examples:
            >>> factory = GeneratorFactory()
            >>> gen = factory.create_from_type('crud', model_name='User')
        """
        if generator_type == GeneratorType.CRUD:
            return GeneratorFactory.create_crud_generator(**kwargs)
        elif generator_type == GeneratorType.BUILTIN:
            return GeneratorFactory.create_builtin_generator(**kwargs)
        else:
            error_msg = f"Unknown generator type: {generator_type}"
            logger.error(error_msg)
            raise ValueError(error_msg)
