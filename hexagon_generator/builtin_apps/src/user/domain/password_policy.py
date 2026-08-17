import re

from src.user.domain.exceptions import InvalidPasswordException

_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)


def validate_password_strength(password: str) -> None:
    """Raise InvalidPasswordException unless the password meets the complexity policy."""
    if not _PASSWORD_PATTERN.match(password):
        raise InvalidPasswordException("Password does not meet the required criteria")
