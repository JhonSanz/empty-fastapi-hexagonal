from src.common.std_response import std_response, StandardResponse
from fastapi import Request, status


class UserNotFoundException(Exception):
    pass


class UserAlreadyExsitException(Exception):
    pass


class InvalidPasswordException(Exception):
    pass


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg=str(exc),
        data=None,
    )


async def user_already_exist_handler(request: Request, exc: UserAlreadyExsitException):
    return std_response(
        status_code=status.HTTP_409_CONFLICT,
        ok=False,
        msg=str(exc),
        data=None,
    )


async def invalid_password_handler(request: Request, exc: InvalidPasswordException):
    return std_response(
        status_code=status.HTTP_409_CONFLICT,
        ok=False,
        msg=str(exc),
        data=None,
    )


EXCEPTIONS_USER_MAPPING = [
    (user_not_found_handler, UserNotFoundException),
    (user_already_exist_handler, UserAlreadyExsitException),
    (invalid_password_handler, InvalidPasswordException),
]
