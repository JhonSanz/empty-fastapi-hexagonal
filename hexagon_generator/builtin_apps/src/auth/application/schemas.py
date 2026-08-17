from pydantic import BaseModel, Field


class AuthUser(BaseModel):
    id: int
    email: str
    password: str
    permissions: list[str] = Field(default_factory=list)


class AuthRequest(BaseModel):
    username: str
    password: str
