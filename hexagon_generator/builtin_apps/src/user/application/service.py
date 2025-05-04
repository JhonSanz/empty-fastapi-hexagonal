import re
import secrets
import string

from bcrypt import checkpw, gensalt, hashpw

from src.user.application.interfaces import UserServiceInterface
from src.user.application.schemas import CreateUserRequest, FilterParams
from src.user.domain.exceptions import (
    InvalidPasswordException,
    UserAlreadyExsitException,
)
from src.user.domain.repository import UserRepository


class UserService(UserServiceInterface):
    def __init__(
        self,
        *,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    def check_password_format(self, password: str) -> bool:
        """
        Validates that the password meets the following criteria:
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character (@$!%*?&)
        - Minimum 8 characters in length
        """
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if not re.match(pattern, password):
            raise InvalidPasswordException(
                "Password does not meet the required criteria"
            )
        return True

    async def generate_random_string(self, *, length) -> str:
        letters = string.ascii_letters + string.digits
        return "".join(secrets.choice(letters) for _ in range(length))

    async def user_by_email_exists(self, email: str) -> bool:
        filter_params = FilterParams(email=email)
        _, count = await self.user_repository.get(filter_params=filter_params)
        if count > 0:
            raise UserAlreadyExsitException(f"User with email {email} already exists")
        return True

    async def user_can_be_created(self, *, user_request: CreateUserRequest) -> None:
        self.check_password_format(password=user_request.password)
        await self.user_by_email_exists(email=user_request.email)
        return True

    def hash_password(self, password: str) -> str:
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    async def check_and_link_roles(self, *, user_id: int, roles: list[int]) -> None:
        if not roles:
            return
        await self.user_repository.check_roles_exist(roles=roles)
        await self.user_repository.bulk_link_roles_to_user(
            user_id=user_id, roles_ids=roles
        )
