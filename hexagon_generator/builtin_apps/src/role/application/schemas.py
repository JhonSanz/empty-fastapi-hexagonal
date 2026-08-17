from pydantic import BaseModel, ConfigDict, Field


class PermissionResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class RoleResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    permissions: list[PermissionResponse] | None = None

    model_config = ConfigDict(from_attributes=True)


class RoleListResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str

    model_config = ConfigDict(from_attributes=True)


class CreateRoleRequest(BaseModel):
    name: str
    permissions: list[int] | None = None

    model_config = ConfigDict(extra="forbid")


class UpdateRoleRequest(BaseModel):
    name: str | None = None
    permissions: list[int] | None = None

    model_config = ConfigDict(extra="forbid")


class FilterParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)
    order_by: str | None = Field(default="id")
    search: str | None = Field(default=None, max_length=100)
    show_permissions: bool | None = False
