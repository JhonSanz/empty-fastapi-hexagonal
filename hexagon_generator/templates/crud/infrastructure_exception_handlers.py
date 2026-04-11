INFRASTRUCTURE_EXCEPTION_HANDLERS_TEMPLATE = """
from fastapi import Request, status

from src.common.std_response import std_response
from src.{{ model_snake_case }}.domain.exceptions import {{ model_pascal_case }}NotFoundException


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
