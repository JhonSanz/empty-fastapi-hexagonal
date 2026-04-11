from dataclasses import dataclass
from typing import Optional


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
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    phone: Optional[str] = None
