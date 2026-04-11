from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from src.common.std_response import std_response

from src.user.infrastructure.exception_handlers import EXCEPTIONS_USER_MAPPING
from src.role.infrastructure.exception_handlers import EXCEPTIONS_ROLE_MAPPING
from src.auth.domain.exceptions import EXCEPTIONS_AUTH_MAPPING


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in errors])
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"ok": False, "msg": f"Validation Error: {msg}", "data": errors},
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    print(exc)
    return std_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ok=False,
        msg="Database error",
        data=None,
    )


async def general_exception_handler(request: Request, exc: Exception):
    print(exc)
    return std_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ok=False,
        msg="An unexpected error occurred",
        data=None,
    )


ALL_EXCEPTIONS = [
    (validation_exception_handler, RequestValidationError),
    (sqlalchemy_error_handler, SQLAlchemyError),
    (general_exception_handler, Exception),
]

ALL_EXCEPTIONS += EXCEPTIONS_USER_MAPPING
ALL_EXCEPTIONS += EXCEPTIONS_ROLE_MAPPING
ALL_EXCEPTIONS += EXCEPTIONS_AUTH_MAPPING
