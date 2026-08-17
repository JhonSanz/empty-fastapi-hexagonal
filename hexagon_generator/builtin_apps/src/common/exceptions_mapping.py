import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from src.common.std_response import std_response

logger = logging.getLogger(__name__)

# TODO: Import your module exception mappings here
# Example:
# from src.product.infrastructure.exception_handlers import EXCEPTIONS_PRODUCT_MAPPING


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in errors])
    return std_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ok=False,
        msg=f"Validation Error: {msg}",
        data=errors,
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    logger.error(
        "Database error while handling %s %s", request.method, request.url, exc_info=exc
    )
    return std_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ok=False,
        msg="Database error",
        data=None,
    )


async def general_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled error while handling %s %s", request.method, request.url, exc_info=exc
    )
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

# TODO: Append your module exception mappings here
# Example:
# ALL_EXCEPTIONS += EXCEPTIONS_PRODUCT_MAPPING
