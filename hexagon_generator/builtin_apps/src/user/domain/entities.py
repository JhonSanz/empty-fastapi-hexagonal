from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool
    is_new: bool
    password: str
    phone: str


@dataclass
class CreateUserData:
    name: str
    email: str
    password: str
    phone: str
    is_active: bool = True
    is_new: bool = True


@dataclass
class UpdateUserData:
    name: str | None = None
    email: str | None = None
    is_active: bool | None = None
    password: str | None = None
    phone: str | None = None
