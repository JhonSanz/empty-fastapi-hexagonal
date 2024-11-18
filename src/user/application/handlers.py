from src.user.application.use_cases.login import LoginUseCase
from src.user.application.schemas import LoginRequest, LoginResponse


def login_handler(
    login_request: LoginRequest, login_use_case: LoginUseCase
) -> LoginResponse:
    token = login_use_case.execute(login_request.username, login_request.password)
    return LoginResponse(token=token).model_dump()
