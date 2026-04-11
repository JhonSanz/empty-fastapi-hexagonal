from fastapi import Request, status

from src.common.std_response import std_response
from src.role.domain.exceptions import RoleNotFoundException, PermissionNotFoundException


async def role_not_found_handler(request: Request, exc: RoleNotFoundException):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg=str(exc),
        data=None,
    )


async def permission_not_found_handler(
    request: Request, exc: PermissionNotFoundException
):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg=str(exc),
        data=None,
    )


EXCEPTIONS_ROLE_MAPPING = [
    (role_not_found_handler, RoleNotFoundException),
    (permission_not_found_handler, PermissionNotFoundException),
]
