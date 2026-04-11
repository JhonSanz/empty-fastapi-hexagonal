import os

import jwt
from bcrypt import gensalt, hashpw

from src.user.domain.repository import UserRepository
from src.user.domain.entities import User, UpdateUserData
from src.user.domain.unit_of_work import UnitOfWork


class ChangePasswordUseCase:
    def __init__(
        self,
        *,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository

    async def execute(self, *, token: str, password: str) -> User:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
        )
        user_id = payload["user"]

        user = await self.user_repository.get_by_id(id=user_id)

        new_password = hashpw(
            password.encode("utf-8"), gensalt()
        ).decode("utf-8")
        data = UpdateUserData(password=new_password)
        await self.user_repository.update(id=user.id, data=data)

        await self.unit_of_work.commit()
        return user
