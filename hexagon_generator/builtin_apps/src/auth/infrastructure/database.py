from src.auth.application.schemas import User
from src.auth.domain.repository import AuthRepository


class UserRepository(AuthRepository):
    def get_user_by_identification(self, identification: str) -> User | None:
        return User(
            id=1,
            email="me@mail.com",
            identification="pez",
            password="$2b$12$XfDb48B1K.CTDxhqDRlJK.TvEwgUrRbFL4.MKMM7VIdcRuykyKc62",
        )
