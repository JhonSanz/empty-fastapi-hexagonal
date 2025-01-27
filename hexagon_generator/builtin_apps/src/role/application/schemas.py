from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class PermissionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RoleInDBBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    permissions: Optional[List[PermissionSchema]] = None


class CreateRoleRequest(BaseModel):
    name: str
    permissions: Optional[List[int]] = None


class UpdateRoleRequest(BaseModel):
    name: str
    permissions: Optional[List[int]] = None


class FilterParams(BaseModel):
    show_permissions: Optional[bool] = False
    skip: int = 0
    limit: int = 10
