from typing import Annotated

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.infrastructure.database import ORMAuthRepository
from src.auth.application.schemas import AuthRequest
from src.common.database_connection import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def get_auth_use_case(db: Session = Depends(get_db)) -> AuthUseCase:
    return AuthUseCase(auth_repo=ORMAuthRepository(db=db))


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
