from dataclasses import dataclass, field


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
    name: str | None = None
