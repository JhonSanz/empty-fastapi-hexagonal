from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PermissionResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class RoleResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    permissions: Optional[list[PermissionResponse]] = None

    model_config = ConfigDict(from_attributes=True)


class RoleListResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str

    model_config = ConfigDict(from_attributes=True)


class CreateRoleRequest(BaseModel):
    name: str
    permissions: Optional[list[int]] = None


class UpdateRoleRequest(BaseModel):
    name: Optional[str] = None
    permissions: Optional[list[int]] = None


class FilterParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)
    order_by: Optional[str] = Field(default="id")
    search: Optional[str] = Field(default=None, max_length=100)
    show_permissions: Optional[bool] = False
