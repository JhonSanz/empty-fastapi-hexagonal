from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    def __init__(self, username: str, password_hash: str):
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, password: str) -> bool:
        return self.password_hash == password
