from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    identification: str
    password: str
