DOMAIN_EXCEPTIONS_TEMPLATE = """from src.common.std_response import std_response, StandardResponse
from fastapi import Request, status


class InvalidTokenException(Exception):
    pass


async def invalid_token_handler(request: Request, exc: InvalidTokenException):
    return std_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        ok=False,
        msg="Invalid token",
        data=None,
    )


class UserNotFoundException(Exception):
    pass


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg="User not found",
        data=None,
    )


EXCEPTIONS_AUTH_MAPPING = [
    (invalid_token_handler, InvalidTokenException),
    (user_not_found_handler, UserNotFoundException),
]

"""