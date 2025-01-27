from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class RoleInDBBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class UserInDBBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    is_active: bool
    roles: list[RoleInDBBase]
    phone: str


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    is_active: bool
    password: str
    roles: list[int]
    phone: str


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    roles: Optional[list[int]] = None
    phone: Optional[str] = None


class FilterParams(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    show_roles: Optional[bool] = False
    skip: int = 0
    limit: int = 10
