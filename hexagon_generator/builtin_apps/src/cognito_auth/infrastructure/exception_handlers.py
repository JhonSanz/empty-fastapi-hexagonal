from fastapi import Request, status

from src.common.std_response import std_response
from src.cognito_auth.domain.exceptions import (
    InvalidTokenException,
    PermissionDeniedException,
    CognitoNotConfiguredException,
)


async def invalid_token_handler(request: Request, exc: InvalidTokenException):
    return std_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        ok=False,
        msg="Invalid token",
        data=None,
    )


async def permission_denied_handler(request: Request, exc: PermissionDeniedException):
    return std_response(
        status_code=status.HTTP_403_FORBIDDEN,
        ok=False,
        msg=str(exc) or "You don't have permission to perform this action",
        data=None,
    )


async def cognito_not_configured_handler(
    request: Request, exc: CognitoNotConfiguredException
):
    return std_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ok=False,
        msg=str(exc),
        data=None,
    )


EXCEPTIONS_COGNITO_AUTH_MAPPING = [
    (invalid_token_handler, InvalidTokenException),
    (permission_denied_handler, PermissionDeniedException),
    (cognito_not_configured_handler, CognitoNotConfiguredException),
]
