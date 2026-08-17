from typing import Annotated

from fastapi import APIRouter, Depends, Form

from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.application.schemas import AuthRequest
from src.auth.dependencies.get_user_with_permissions import get_auth_use_case


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/token")
async def login(
    auth_request: Annotated[AuthRequest, Form()],
    auth_use_case: AuthUseCase = Depends(get_auth_use_case),
):
    token = await auth_use_case.authenticate_user(
        email=auth_request.username,
        password=auth_request.password,
    )
    return {"access_token": token, "token_type": "bearer"}
