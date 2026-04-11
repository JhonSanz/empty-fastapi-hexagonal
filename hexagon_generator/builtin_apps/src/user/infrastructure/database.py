from dataclasses import asdict

from sqlalchemy import select, update, delete, func, or_, desc, asc
from sqlalchemy.orm import Session, joinedload

from src.user.domain.repository import UserRepository
from src.user.domain.entities import User, CreateUserData, UpdateUserData
from src.user.domain.exceptions import UserNotFoundException
from src.user.infrastructure.models import UserORM, UserRoleAssociation
from src.role.infrastructure.models import RoleORM


class ORMUserRepository(UserRepository):
    def __init__(self, *, db: Session):
        self.db = db

    @staticmethod
    def _to_entity(orm_obj: UserORM) -> User:
        return User(
            id=orm_obj.id,
            name=orm_obj.name,
            email=orm_obj.email,
            is_active=orm_obj.is_active,
            is_new=orm_obj.is_new,
            password=orm_obj.password,
            phone=orm_obj.phone,
        )

    async def get_by_id(self, *, id: int) -> User:
        stmt = select(UserORM).where(UserORM.id == id)
        result = self.db.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if not orm_obj:
            raise UserNotFoundException(f"User with ID {id} not found")

        return self._to_entity(orm_obj)

    async def get(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        search: str | None = None,
        **filters,
    ) -> tuple[list[User], int]:
        stmt = select(UserORM)

        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(
                or_(
                    UserORM.name.ilike(search_pattern),
                    UserORM.email.ilike(search_pattern),
                )
            )

        if email := filters.get("email"):
            stmt = stmt.where(UserORM.email == email)
        if name := filters.get("name"):
            stmt = stmt.where(UserORM.name.ilike(f"%{name}%"))
        if (is_active := filters.get("is_active")) is not None:
            stmt = stmt.where(UserORM.is_active == is_active)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        count = self.db.execute(count_stmt).scalar()

        if order_by:
            order_field = order_by.lstrip("-")
            is_desc = order_by.startswith("-")
            if hasattr(UserORM, order_field):
                order_column = getattr(UserORM, order_field)
                stmt = stmt.order_by(
                    desc(order_column) if is_desc else asc(order_column)
                )
        else:
            stmt = stmt.order_by(desc(UserORM.id))

        stmt = stmt.offset(skip).limit(limit)

        result = self.db.execute(stmt)
        orm_objects = result.scalars().all()

        return [self._to_entity(obj) for obj in orm_objects], count

    async def create(self, *, data: CreateUserData) -> User:
        data_dict = asdict(data)
        orm_obj = UserORM(**data_dict)

        self.db.add(orm_obj)
        self.db.flush()
        self.db.refresh(orm_obj)

        return self._to_entity(orm_obj)

    async def update(self, *, id: int, data: UpdateUserData) -> User:
        await self.get_by_id(id=id)

        update_data = {k: v for k, v in asdict(data).items() if v is not None}

        if not update_data:
            return await self.get_by_id(id=id)

        stmt = update(UserORM).where(UserORM.id == id).values(**update_data)
        self.db.execute(stmt)
        self.db.flush()

        return await self.get_by_id(id=id)

    async def delete(self, *, id: int) -> User:
        entity = await self.get_by_id(id=id)

        self.db.execute(
            delete(UserRoleAssociation).where(UserRoleAssociation.user_id == id)
        )
        self.db.execute(delete(UserORM).where(UserORM.id == id))
        self.db.flush()

        return entity

    async def get_by_email(self, *, email: str) -> User | None:
        stmt = select(UserORM).where(UserORM.email == email)
        result = self.db.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if not orm_obj:
            return None
        return self._to_entity(orm_obj)

    async def check_roles_exist(self, *, roles: list[int]) -> None:
        from src.role.domain.exceptions import RoleNotFoundException

        stmt = select(RoleORM.id).where(RoleORM.id.in_(roles))
        result = self.db.execute(stmt)
        existing_ids = {row[0] for row in result}

        missing_ids = set(roles) - existing_ids
        if missing_ids:
            raise RoleNotFoundException(f"Roles with ids {missing_ids} do not exist.")

    async def bulk_link_roles_to_user(
        self, *, user_id: int, roles_ids: list[int]
    ) -> None:
        self.db.execute(
            delete(UserRoleAssociation).where(UserRoleAssociation.user_id == user_id)
        )
        self.db.flush()
        new_associations = [
            UserRoleAssociation(role_id=role_id, user_id=user_id)
            for role_id in roles_ids
        ]
        self.db.bulk_save_objects(new_associations)
