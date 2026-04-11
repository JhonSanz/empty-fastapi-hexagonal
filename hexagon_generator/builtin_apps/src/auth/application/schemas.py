from pydantic import BaseModel


class AuthUser(BaseModel):
    id: int
    email: str
    password: str


class AuthRequest(BaseModel):
    username: str
    password: str
