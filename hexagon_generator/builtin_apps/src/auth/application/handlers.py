from src.auth.application.use_cases.auth import AuthUseCase


async def auth_handler(
    *, auth_use_case: AuthUseCase, identification: str, password: str
) -> str:
    token = await auth_use_case.authenticate_user(
        identification=identification, password=password
    )
    return token