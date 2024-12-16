INFRASTRUCTURE_WEB_TEMPLATE = """import os
from typing import Annotated
from fastapi import APIRouter, Depends, Form
from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.infrastructure.database import UserRepository
from src.auth.application.service import AuthService
from src.common.database_connection import get_db
from src.auth.application.handlers import auth_handler
from src.auth.application.schemas import AuthRequest


router = APIRouter()


@router.post("/token")
async def login(auth_request: Annotated[AuthRequest, Form()], database=Depends(get_db)):
    auth_service = AuthService(
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
        access_token_expire_minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
    )
    user_repo = UserRepository()
    auth_use_case = AuthUseCase(
        database=database, auth_repo=user_repo, auth_service=auth_service
    )
    token = await auth_handler(
        identification=auth_request.username,
        password=auth_request.password,
        auth_use_case=auth_use_case,
    )
    return {"access_token": token, "token_type": "bearer"}

"""