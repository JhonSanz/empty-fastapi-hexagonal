DOMAIN_EXCEPTIONS_TEMPLATE = """
from src.common.std_response import std_response, StandardResponse
from fastapi import Request, status


class {{ model_pascal_case }}NotFoundException(Exception):
    pass

async def {{ model_snake_case }}_not_found_handler(request: Request, exc: {{ model_pascal_case }}NotFoundException):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg=str(exc),
        data=None,
    )

EXCEPTIONS_{{ model_pascal_case.upper() }}_MAPPING = [
    ({{ model_snake_case }}_not_found_handler, {{ model_pascal_case }}NotFoundException),
]
"""