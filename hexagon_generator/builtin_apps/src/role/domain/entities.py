from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Permission:
    id: int
    name: str


@dataclass
class Role:
    id: int
    name: str
    permissions: list[Permission] = field(default_factory=list)


@dataclass
class CreateRoleData:
    name: str


@dataclass
class UpdateRoleData:
    name: Optional[str] = None
