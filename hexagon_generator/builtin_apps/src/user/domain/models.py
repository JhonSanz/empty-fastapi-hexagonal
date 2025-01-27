from sqlalchemy import Integer, PrimaryKeyConstraint, Boolean, Text, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from src.common.database_connection import Base

from src.common.database_connection import Base


class UserRoleAssociation(Base):
    __tablename__ = "UserRoleAssociation"

    user_id = mapped_column(Integer, ForeignKey("User.id"), primary_key=True)
    role_id = mapped_column(Integer, ForeignKey("Role.id"), primary_key=True)


class User(Base):
    __tablename__ = "User"
    __table_args__ = (PrimaryKeyConstraint("id", name="User_pkey"),)

    id = mapped_column(Integer)
    name = mapped_column(Text, nullable=False)
    email = mapped_column(Text, nullable=False)
    is_active = mapped_column(Boolean, default=True)
    password = mapped_column(Text, nullable=False)
    phone = mapped_column(Text, nullable=False)

    roles = relationship(
        "Role", secondary="UserRoleAssociation", back_populates="users", lazy="noload"
    )
