from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.database_connection import Base


class UserRoleAssociation(Base):
    __tablename__ = "UserRoleAssociation"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("User.id"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Role.id"), primary_key=True
    )


class UserORM(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_new: Mapped[bool] = mapped_column(Boolean, default=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)

    roles = relationship(
        "RoleORM",
        secondary="UserRoleAssociation",
        back_populates="users",
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<UserORM(id={self.id}, email={self.email})>"
