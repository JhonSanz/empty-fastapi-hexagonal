from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, description="User name")
    email: EmailStr = Field(..., description="User email")
    phone: str = Field(..., description="User phone number")


class CreateUserRequest(UserBase):
    password: str = Field(..., min_length=8, description="User password")
    is_active: bool = Field(default=True)
    roles: list[int] = Field(default_factory=list)


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    roles: Optional[list[int]] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    id: int = Field(..., gt=0)
    is_active: bool
    is_new: bool

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class FilterParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)
    order_by: Optional[str] = Field(default="id")
    search: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
