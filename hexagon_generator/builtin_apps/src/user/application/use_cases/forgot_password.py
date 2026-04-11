import os
import secrets
import string
from datetime import datetime, timedelta

import jwt
from bcrypt import gensalt, hashpw

from src.user.domain.repository import UserRepository
from src.user.domain.entities import UpdateUserData
from src.user.domain.unit_of_work import UnitOfWork
from src.user.domain.exceptions import UserNotFoundException


class ForgotPasswordUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository

    async def execute(self, *, email: str) -> str:
        user = await self.user_repository.get_by_email(email=email)
        if not user:
            raise UserNotFoundException(f"Usuario con correo {email} no existe")

        random_string = self._generate_random_string(length=16)
        new_password = hashpw(
            random_string.encode("utf-8"), gensalt()
        ).decode("utf-8")

        data = UpdateUserData(password=new_password)
        await self.user_repository.update(id=user.id, data=data)

        token = self._create_token(
            data={"user": user.id, "new_password": new_password}
        )
        await self.unit_of_work.commit()
        return token

    @staticmethod
    def _generate_random_string(*, length: int) -> str:
        letters = string.ascii_letters + string.digits
        return "".join(secrets.choice(letters) for _ in range(length))

    @staticmethod
    def _create_token(*, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            os.getenv("SECRET_KEY"),
            algorithm=os.getenv("ALGORITHM"),
        )
