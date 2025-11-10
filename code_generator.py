"""
Hexagonal Architecture Code Generator for FastAPI.

Generates complete CRUD modules or copies built-in applications
following hexagonal architecture patterns.
"""

import argparse
import logging
import sys
from typing import Optional

from hexagon_generator.core.config import BUILTIN_APPS_CONFIG, CRUD_CONFIG
from hexagon_generator.core.generator_factory import GeneratorFactory, GeneratorType
from hexagon_generator.utils import NamingError, suggest_name_fix

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Generador de archivos hexagonales para FastAPI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate CRUD for a model (auto-converts naming)
  python code_generator.py crud User
  python code_generator.py crud user_account

  # Generate CRUD with specific actions
  python code_generator.py crud Product --actions create list retrieve

  # Copy a built-in application
  python code_generator.py builtin user

  # Verbose output
  python code_generator.py crud Order -v
        """,
    )

    # Main command
    parser.add_argument(
        "type",
        type=str,
        choices=[GeneratorType.CRUD, GeneratorType.BUILTIN],
        help="Generator type: 'crud' for CRUD generation, 'builtin' for built-in apps",
    )

    # Model name (for CRUD)
    parser.add_argument(
        "model_name",
        type=str,
        nargs="?",
        help="Model name (PascalCase or snake_case, auto-converted)",
    )

    # Optional arguments
    parser.add_argument(
        "--actions",
        nargs="+",
        default=None,
        help=f"HTTP actions to generate (default: {', '.join(CRUD_CONFIG.actions)})",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (DEBUG level)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without creating files",
    )

    return parser


def validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """
    Validate command-line arguments.

    Args:
        args: Parsed arguments
        parser: ArgumentParser instance for error reporting

    Raises:
        SystemExit: If arguments are invalid
    """
    if args.type == GeneratorType.CRUD:
        if not args.model_name:
            parser.error("For 'crud' type, 'model_name' argument is required.")

    elif args.type == GeneratorType.BUILTIN:
        if not args.model_name:
            parser.error("For 'builtin' type, app name is required.")

        # Validate app name
        if not BUILTIN_APPS_CONFIG.is_valid_app(args.model_name):
            available = ", ".join(BUILTIN_APPS_CONFIG.available_apps)
            parser.error(
                f"Invalid built-in app: '{args.model_name}'. "
                f"Available apps: {available}"
            )


def handle_crud_generation(model_name: str, actions: Optional[list[str]] = None) -> None:
    """
    Handle CRUD generation.

    Args:
        model_name: Model name (can be PascalCase or snake_case)
        actions: Optional list of CRUD actions
    """
    try:
        factory = GeneratorFactory()
        generator = factory.create_crud_generator(
            model_name=model_name,
            actions=actions,
        )
        generator.run()
        logger.info(f"✓ CRUD generation completed for {model_name}")

    except NamingError as e:
        logger.error(f"Invalid model name: {e}")
        suggestion = suggest_name_fix(model_name)
        if suggestion:
            logger.info(f"Did you mean: {suggestion}?")
        sys.exit(1)
    except Exception as e:
        logger.error(f"CRUD generation failed: {e}")
        if logging.getLogger().level == logging.DEBUG:
            logger.exception("Full traceback:")
        sys.exit(1)


def handle_builtin_generation(app_name: str) -> None:
    """
    Handle built-in app generation.

    Args:
        app_name: Name of the built-in app
    """
    try:
        factory = GeneratorFactory()
        generator, source_path, target_path = factory.create_builtin_generator(app_name)
        generator.copy_builtin_apps(
            path_source=source_path,
            path_target=target_path,
        )
        logger.info(f"✓ Built-in app '{app_name}' copied successfully")

    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Built-in app generation failed: {e}")
        if logging.getLogger().level == logging.DEBUG:
            logger.exception("Full traceback:")
        sys.exit(1)


def main() -> None:
    """Main entry point for the code generator."""
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")

    # Validate arguments
    validate_args(args, parser)

    # Show dry-run notice
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be created")
        # TODO: Implement dry-run functionality
        logger.warning("Dry-run not yet implemented")
        return

    try:
        # Always create base structure first
        logger.info("Creating base project structure...")
        factory = GeneratorFactory()
        base_generator = factory.create_base_generator()
        base_generator.run()

        # Handle specific generator type
        if args.type == GeneratorType.CRUD:
            handle_crud_generation(args.model_name, args.actions)

        elif args.type == GeneratorType.BUILTIN:
            handle_builtin_generation(args.model_name)

    except KeyboardInterrupt:
        logger.warning("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if logging.getLogger().level == logging.DEBUG:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
