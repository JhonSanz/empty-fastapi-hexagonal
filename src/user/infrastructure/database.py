from src.user.domain.repository import UserRepository
from src.user.domain.models import User

# from sqlalchemy.orm import Session


class ORMUserRepository(UserRepository):
    # def __init__(self, db: Session):
    def __init__(self, *, db):
        self.db = db

    def find_by_username(self, username: str) -> User:
        # return self.db.query(User).filter(User.username == username).first()
        return {"username": "john doe", "password": "myawesomepassword"}

    def save(self, user: User):
        # self.db.add(user)
        # self.db.commit()
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def find_by_username(self, username: str):
        return self.users.get(username)

    def save(self, user: "User"):
        self.users[user.username] = user
