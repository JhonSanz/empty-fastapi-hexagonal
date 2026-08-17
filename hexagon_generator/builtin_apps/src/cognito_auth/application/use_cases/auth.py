from src.cognito_auth.application.schemas import CognitoUser
from src.cognito_auth.domain.repository import AuthRepository
from src.cognito_auth.domain.exceptions import InvalidTokenException
from src.cognito_auth.infrastructure.cognito_verifier import get_verifier
from src.cognito_user.domain.entities import CreateUserData
from src.cognito_user.domain.repository import UserRepository
from src.cognito_user.domain.unit_of_work import UnitOfWork
from src.cognito_user.application.use_cases.create import CreateUseCase


class CognitoAuthUseCase:
    """
    Resolves the caller's identity from a Cognito ID token.

    On first sight of a given `cognito_sub`, JIT-provisions the local
    shadow `User` row (no roles assigned by default — an admin has to grant
    those afterwards through `cognito_user`'s update endpoint).
    """

    def __init__(
        self,
        *,
        auth_repo: AuthRepository,
        user_repository: UserRepository,
        unit_of_work: UnitOfWork,
    ):
        self.auth_repo = auth_repo
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work

    async def get_current_user(self, *, token: str) -> CognitoUser:
        payload = get_verifier().verify(token)

        cognito_sub = payload.get("sub")
        email = payload.get("email")
        if not cognito_sub or not email:
            raise InvalidTokenException("Token is missing required claims")

        user = await self.auth_repo.get_user_by_cognito_sub(cognito_sub=cognito_sub)
        if user is not None:
            return user

        return await self._provision_user(
            cognito_sub=cognito_sub,
            email=email,
            name=payload.get("name") or email,
            phone=payload.get("phone_number") or "",
        )

    async def _provision_user(
        self, *, cognito_sub: str, email: str, name: str, phone: str
    ) -> CognitoUser:
        create_use_case = CreateUseCase(
            unit_of_work=self.unit_of_work,
            user_repository=self.user_repository,
        )
        await create_use_case.execute(
            data=CreateUserData(
                cognito_sub=cognito_sub, email=email, name=name, phone=phone
            )
        )
        # Re-fetch through auth_repo so permissions (empty, for a brand new
        # user) come back populated in the same shape as an existing user.
        return await self.auth_repo.get_user_by_cognito_sub(cognito_sub=cognito_sub)
