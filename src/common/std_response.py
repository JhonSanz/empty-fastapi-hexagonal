from typing import Generic, TypeVar, List, Optional
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: Optional[str] = ""
    result: Optional[T] = None
    count: int = 0


def std_response(
    *,
    status_code=status.HTTP_200_OK,
    ok: bool = True,
    msg: str = "",
    data: Optional[T] = None,
    count: int = 0
):
    if ok:
        return StandardResponse(success=ok, message=msg, result=data, count=count)
    # https://fastapi.tiangolo.com/advanced/response-change-status-code/#use-a-response-parameter
    return JSONResponse(
        status_code=status_code,
        content=StandardResponse(success=ok, message=msg, result=None).model_dump(),
    )
