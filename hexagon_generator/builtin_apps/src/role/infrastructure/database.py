from sqlalchemy import select, update, delete, func, desc, asc
from sqlalchemy.orm import Session, joinedload

from src.role.domain.repository import RoleRepository
from src.role.domain.entities import (
    Role,
    Permission,
    CreateRoleData,
    UpdateRoleData,
)
from src.role.domain.exceptions import RoleNotFoundException, PermissionNotFoundException
from src.role.infrastructure.models import (
    RoleORM,
    PermissionORM,
    RolePermissionAssociation,
)


class ORMRoleRepository(RoleRepository):
    def __init__(self, *, db: Session):
        self.db = db

    @staticmethod
    def _to_entity(orm_obj: RoleORM, *, with_permissions: bool = False) -> Role:
        permissions = []
        if with_permissions and orm_obj.permissions:
            permissions = [
                Permission(id=p.id, name=p.name) for p in orm_obj.permissions
            ]
        return Role(
            id=orm_obj.id,
            name=orm_obj.name,
            permissions=permissions,
        )

    @staticmethod
    def _permission_to_entity(orm_obj: PermissionORM) -> Permission:
        return Permission(id=orm_obj.id, name=orm_obj.name)

    async def get_by_id(self, *, id: int) -> Role:
        stmt = select(RoleORM).where(RoleORM.id == id)
        result = self.db.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if not orm_obj:
            raise RoleNotFoundException(f"Role with ID {id} not found")

        return self._to_entity(orm_obj)

    async def get(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
        order_by: str | None = None,
        search: str | None = None,
        show_permissions: bool = False,
        **filters,
    ) -> tuple[list[Role], int]:
        stmt = select(RoleORM)

        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(RoleORM.name.ilike(search_pattern))

        if show_permissions:
            stmt = stmt.options(joinedload(RoleORM.permissions))

        count_stmt = select(func.count()).select_from(
            select(RoleORM.id).where(stmt.whereclause) if stmt.whereclause is not None
            else select(RoleORM.id)
        )
        count = self.db.execute(count_stmt).scalar()

        if order_by:
            order_field = order_by.lstrip("-")
            is_desc = order_by.startswith("-")
            if hasattr(RoleORM, order_field):
                order_column = getattr(RoleORM, order_field)
                stmt = stmt.order_by(
                    desc(order_column) if is_desc else asc(order_column)
                )
        else:
            stmt = stmt.order_by(desc(RoleORM.id))

        stmt = stmt.offset(skip).limit(limit)

        result = self.db.execute(stmt)
        orm_objects = result.unique().scalars().all()

        return [
            self._to_entity(obj, with_permissions=show_permissions)
            for obj in orm_objects
        ], count

    async def create(self, *, data: CreateRoleData) -> Role:
        orm_obj = RoleORM(name=data.name)

        self.db.add(orm_obj)
        self.db.flush()
        self.db.refresh(orm_obj)

        return self._to_entity(orm_obj)

    async def update(self, *, id: int, data: UpdateRoleData) -> Role:
        await self.get_by_id(id=id)

        update_data = {}
        if data.name is not None:
            update_data["name"] = data.name

        if not update_data:
            return await self.get_by_id(id=id)

        stmt = update(RoleORM).where(RoleORM.id == id).values(**update_data)
        self.db.execute(stmt)
        self.db.flush()

        return await self.get_by_id(id=id)

    async def delete(self, *, id: int) -> Role:
        entity = await self.get_by_id(id=id)

        self.db.execute(
            delete(RolePermissionAssociation).where(
                RolePermissionAssociation.role_id == id
            )
        )
        self.db.execute(delete(RoleORM).where(RoleORM.id == id))
        self.db.flush()

        return entity

    async def get_permissions(self) -> tuple[list[Permission], int]:
        stmt = select(PermissionORM)
        count_stmt = select(func.count()).select_from(PermissionORM)
        count = self.db.execute(count_stmt).scalar()

        result = self.db.execute(stmt)
        orm_objects = result.scalars().all()

        return [self._permission_to_entity(obj) for obj in orm_objects], count

    async def check_permissions_exist(self, *, permissions: list[int]) -> None:
        stmt = select(PermissionORM.id).where(PermissionORM.id.in_(permissions))
        result = self.db.execute(stmt)
        existing_ids = {row[0] for row in result}

        missing_ids = set(permissions) - existing_ids
        if missing_ids:
            raise PermissionNotFoundException(
                f"Permissions with ids {missing_ids} do not exist."
            )

    async def bulk_link_permissions_to_role(
        self, *, role_id: int, permission_ids: list[int]
    ) -> None:
        self.db.execute(
            delete(RolePermissionAssociation).where(
                RolePermissionAssociation.role_id == role_id
            )
        )
        self.db.flush()
        new_associations = [
            RolePermissionAssociation(role_id=role_id, permission_id=permission_id)
            for permission_id in permission_ids
        ]
        self.db.bulk_save_objects(new_associations)
