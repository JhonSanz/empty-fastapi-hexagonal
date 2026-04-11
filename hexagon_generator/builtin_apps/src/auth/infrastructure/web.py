from typing import Annotated

from fastapi import APIRouter, Depends, Form

from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.infrastructure.database import UserRepository
from src.auth.application.schemas import AuthRequest


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/token")
async def login(auth_request: Annotated[AuthRequest, Form()]):
    user_repo = UserRepository()
    auth_use_case = AuthUseCase(auth_repo=user_repo)
    token = await auth_use_case.authenticate_user(
        identification=auth_request.username,
        password=auth_request.password,
    )
    return {"access_token": token, "token_type": "bearer"}
