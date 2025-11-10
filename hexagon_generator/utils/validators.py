"""Utilities for validating and converting naming conventions."""

import re
from typing import Optional


class NamingError(Exception):
    """Exception raised when naming validation fails."""
    pass


def validate_pascal_case(name: str) -> bool:
    """
    Validate that a string follows PascalCase convention.

    Args:
        name: String to validate

    Returns:
        True if valid PascalCase, False otherwise

    Examples:
        >>> validate_pascal_case("UserAccount")
        True
        >>> validate_pascal_case("userAccount")
        False
    """
    if not name:
        return False

    # PascalCase: starts with uppercase, contains only alphanumeric
    pattern = r'^[A-Z][a-zA-Z0-9]*$'
    return bool(re.match(pattern, name))


def validate_snake_case(name: str) -> bool:
    """
    Validate that a string follows snake_case convention.

    Args:
        name: String to validate

    Returns:
        True if valid snake_case, False otherwise

    Examples:
        >>> validate_snake_case("user_account")
        True
        >>> validate_snake_case("UserAccount")
        False
    """
    if not name:
        return False

    # snake_case: lowercase letters, numbers, and underscores only
    pattern = r'^[a-z][a-z0-9_]*$'
    return bool(re.match(pattern, name))


def pascal_to_snake_case(pascal_case: str) -> str:
    """
    Convert PascalCase string to snake_case.

    Args:
        pascal_case: String in PascalCase format

    Returns:
        String converted to snake_case

    Raises:
        NamingError: If input is not valid PascalCase

    Examples:
        >>> pascal_to_snake_case("UserAccount")
        'user_account'
        >>> pascal_to_snake_case("HTTPResponse")
        'http_response'
    """
    if not validate_pascal_case(pascal_case):
        raise NamingError(f"'{pascal_case}' is not valid PascalCase")

    # Insert underscore before uppercase letters (except first one)
    snake = re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_case)
    return snake.lower()


def snake_to_pascal_case(snake_case: str) -> str:
    """
    Convert snake_case string to PascalCase.

    Args:
        snake_case: String in snake_case format

    Returns:
        String converted to PascalCase

    Raises:
        NamingError: If input is not valid snake_case

    Examples:
        >>> snake_to_pascal_case("user_account")
        'UserAccount'
        >>> snake_to_pascal_case("http_response")
        'HttpResponse'
    """
    if not validate_snake_case(snake_case):
        raise NamingError(f"'{snake_case}' is not valid snake_case")

    # Split by underscore and capitalize each word
    words = snake_case.split('_')
    return ''.join(word.capitalize() for word in words)


def normalize_name(name: str) -> tuple[str, str]:
    """
    Normalize a name to both PascalCase and snake_case.

    Automatically detects the input format and converts to both conventions.

    Args:
        name: String in either PascalCase or snake_case

    Returns:
        Tuple of (pascal_case, snake_case)

    Raises:
        NamingError: If input is neither valid PascalCase nor snake_case

    Examples:
        >>> normalize_name("UserAccount")
        ('UserAccount', 'user_account')
        >>> normalize_name("user_account")
        ('UserAccount', 'user_account')
    """
    if validate_pascal_case(name):
        return name, pascal_to_snake_case(name)
    elif validate_snake_case(name):
        return snake_to_pascal_case(name), name
    else:
        raise NamingError(
            f"'{name}' is neither valid PascalCase nor snake_case. "
            "Expected formats: 'UserAccount' or 'user_account'"
        )


def suggest_name_fix(name: str) -> Optional[str]:
    """
    Suggest a corrected name if the input is close to a valid format.

    Args:
        name: Potentially invalid name

    Returns:
        Suggested correction, or None if no suggestion available

    Examples:
        >>> suggest_name_fix("user-account")
        'user_account'
        >>> suggest_name_fix("User_Account")
        'UserAccount'
    """
    # Remove invalid characters
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', name)

    # Try to detect intention
    if '_' in cleaned:
        # Likely intended as snake_case
        return cleaned.lower()
    elif cleaned[0].isupper() if cleaned else False:
        # Likely intended as PascalCase
        return ''.join(c for c in cleaned if c != '_')

    return None
