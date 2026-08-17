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
    """
    Local shadow profile for a Cognito-authenticated identity.

    Table/class names match the local (`src.user`) variant on purpose so
    `RoleORM`'s `secondary="UserRoleAssociation"` relationship resolves the
    same way regardless of which auth flavor a project uses. Never generate
    both `user` and `cognito_user` into the same project.
    """

    __tablename__ = "User"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cognito_sub: Mapped[str] = mapped_column(Text, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    roles = relationship(
        "RoleORM",
        secondary="UserRoleAssociation",
        back_populates="users",
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, cognito_sub={self.cognito_sub})>"
