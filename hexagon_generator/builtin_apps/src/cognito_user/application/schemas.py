from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    id: int = Field(..., gt=0)
    cognito_sub: str
    name: str
    email: str
    phone: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    is_active: bool | None = None
    roles: list[int] | None = None

    model_config = ConfigDict(extra="forbid")


class FilterParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)
    order_by: str | None = Field(default="id")
    search: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None
