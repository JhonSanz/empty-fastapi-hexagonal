from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    identification: str
    password: str


class AuthRequest(BaseModel):
    username: str
    password: str
