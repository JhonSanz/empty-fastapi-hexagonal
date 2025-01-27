from sqlalchemy import (
    Integer,
    PrimaryKeyConstraint,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from src.common.database_connection import Base


class RolePermissionAssociation(Base):
    __tablename__ = "RolePermissionAssociation"

    role_id = mapped_column(Integer, ForeignKey("Role.id"), primary_key=True)
    permission_id = mapped_column(
        Integer, ForeignKey("Permission.id"), primary_key=True
    )


class Role(Base):
    __tablename__ = "Role"
    __table_args__ = (PrimaryKeyConstraint("id", name="Role_pkey"),)

    id = mapped_column(Integer)
    name = mapped_column(Text, nullable=False)

    permissions = relationship(
        "Permission",
        secondary="RolePermissionAssociation",
        back_populates="roles",
        lazy="noload"
    )

    users = relationship(
        "User",
        secondary="UserRoleAssociation",
        back_populates="roles"
    )


class Permission(Base):
    __tablename__ = "Permission"
    __table_args__ = (PrimaryKeyConstraint("id", name="Permission_pkey"),)

    id = mapped_column(Integer)
    name = mapped_column(Text, nullable=False)

    roles = relationship(
        "Role",
        secondary="RolePermissionAssociation",
        back_populates="permissions",
    )
