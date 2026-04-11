from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.database_connection import Base


class RolePermissionAssociation(Base):
    __tablename__ = "RolePermissionAssociation"

    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Role.id"), primary_key=True
    )
    permission_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Permission.id"), primary_key=True
    )


class RoleORM(Base):
    __tablename__ = "Role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    permissions = relationship(
        "PermissionORM",
        secondary="RolePermissionAssociation",
        back_populates="roles",
        lazy="noload",
    )

    users = relationship(
        "UserORM",
        secondary="UserRoleAssociation",
        back_populates="roles",
    )

    def __repr__(self) -> str:
        return f"<RoleORM(id={self.id}, name={self.name})>"


class PermissionORM(Base):
    __tablename__ = "Permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    roles = relationship(
        "RoleORM",
        secondary="RolePermissionAssociation",
        back_populates="permissions",
    )

    def __repr__(self) -> str:
        return f"<PermissionORM(id={self.id}, name={self.name})>"
