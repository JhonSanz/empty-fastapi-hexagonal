from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, description="User name")
    email: EmailStr = Field(..., description="User email")
    phone: str = Field(..., description="User phone number")


class CreateUserRequest(UserBase):
    password: str = Field(..., min_length=8, description="User password")
    is_active: bool = Field(default=True)
    roles: list[int] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    password: str | None = None
    roles: list[int] | None = None
    phone: str | None = None

    model_config = ConfigDict(extra="forbid")


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
    order_by: str | None = Field(default="id")
    search: str | None = Field(default=None, max_length=100)
    email: str | None = None
    name: str | None = None
    is_active: bool | None = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    model_config = ConfigDict(extra="forbid")


class ChangePasswordRequest(BaseModel):
    token: str
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(extra="forbid")
