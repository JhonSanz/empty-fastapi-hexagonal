from fastapi import APIRouter, Depends
from src.user.application.schemas import LoginRequest, LoginResponse
from src.user.application.handlers import login_handler
from src.user.application.use_cases.login import LoginUseCase
from src.user.infrastructure.database import ORMUserRepository
from src.user.domain.service import UserService

router = APIRouter()


# @router.post("/login", response_model=LoginResponse)
# def login_endpoint(login_request: LoginRequest):
def login_endpoint():
    login_request = LoginRequest(**{
        "username": "john doe",
        "password": "john doe"
    })
    # user_repo = ORMUserRepository(db_session)
    user_repo = ORMUserRepository(db=None)
    user_service = UserService()
    login_use_case = LoginUseCase(user_repository=user_repo, user_service=user_service)
    return login_handler(login_request, login_use_case=login_use_case)
