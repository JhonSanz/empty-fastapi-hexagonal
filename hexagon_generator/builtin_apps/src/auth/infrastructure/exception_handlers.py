from fastapi import Request, status

from src.common.std_response import std_response
from src.auth.domain.exceptions import (
    InvalidTokenException,
    UserNotFoundException,
    PermissionDeniedException,
)


async def invalid_token_handler(request: Request, exc: InvalidTokenException):
    return std_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        ok=False,
        msg="Invalid token",
        data=None,
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg="User not found",
        data=None,
    )


async def permission_denied_handler(request: Request, exc: PermissionDeniedException):
    return std_response(
        status_code=status.HTTP_403_FORBIDDEN,
        ok=False,
        msg=str(exc) or "You don't have permission to perform this action",
        data=None,
    )


EXCEPTIONS_AUTH_MAPPING = [
    (invalid_token_handler, InvalidTokenException),
    (user_not_found_handler, UserNotFoundException),
    (permission_denied_handler, PermissionDeniedException),
]
