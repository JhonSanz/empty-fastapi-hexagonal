from sqlalchemy.orm import joinedload, load_only
from src.role.domain.repository import RoleRepository
from src.role.domain.models import Role, Permission, RolePermissionAssociation
from src.role.application.schemas import (
    CreateRoleRequest,
    UpdateRoleRequest,
    FilterParams,
)
from src.role.domain.exceptions import (
    RoleNotFoundException,
    PermissionNotFoundException,
)


class ORMRoleRepository(RoleRepository):
    def __init__(self, *, db):
        self.db = db

    async def get_by_id(self, *, id: int, filter_params: FilterParams) -> Role:
        existing_role = self.db.query(Role).filter(Role.id == id)
        if filter_params.show_permissions:
            existing_role = existing_role.options(joinedload(Role.permissions))

        existing_role = existing_role.first()
        if not existing_role:
            raise RoleNotFoundException(f"Role {id} not found")
        return existing_role

    async def get(self, *, filter_params: FilterParams) -> tuple[list[Role], int]:
        role_query = self.db.query(Role).options(load_only(Role.id, Role.name))

        if filter_params.show_permissions:
            role_query = role_query.options(joinedload(Role.permissions))

        count = role_query.count()
        roles = role_query.offset(filter_params.skip).limit(filter_params.limit).all()
        return roles, count

    async def create(self, *, data: CreateRoleRequest):
        data_ = data.model_dump(exclude={"permissions"})
        role_result = Role(**data_)
        self.db.add(role_result)
        self.db.flush()
        self.db.refresh(role_result)
        return role_result

    async def update(self, *, id: int, data: UpdateRoleRequest):
        data_ = data.model_dump(exclude_none=True, exclude={"permissions"})
        role_result = (
            self.db.query(Role)
            .filter(Role.id == id)
            .update(data_, synchronize_session="fetch")
        )

        if role_result == 0:
            raise RoleNotFoundException(f"Role with ID {id} not found")

        updated_role = self.db.query(Role).filter(Role.id == id).first()
        self.db.refresh(updated_role)
        return updated_role

    async def delete(self, *, id: int):
        existing_role = self.db.query(Role).filter(Role.id == id).first()
        if not existing_role:
            raise RoleNotFoundException(f"Role with ID {id} not found")

        self.db.query(RolePermissionAssociation).filter(
            RolePermissionAssociation.role_id == id
        ).delete()
        self.db.delete(existing_role)
        self.db.flush()

    async def check_roles_exist(self, *, roles: list[int]):
        existing_roles = self.db.query(Role.id).filter(Role.id.in_(roles)).all()
        existing_ids = {role_id[0] for role_id in existing_roles}

        missing_ids = set(roles) - existing_ids
        if missing_ids:
            raise RoleNotFoundException(f"Roles with ids {missing_ids} do not exist.")

    async def get_permissions(self) -> tuple[list[Permission], int]:
        permission_query = self.db.query(Permission)
        count = permission_query.count()
        permissions = permission_query.all()
        return permissions, count

    async def check_permissions_exist(self, permissions: list[int]) -> None:
        existing_permissions = (
            self.db.query(Permission.id).filter(Permission.id.in_(permissions)).all()
        )
        existing_ids = {perm_id[0] for perm_id in existing_permissions}

        missing_ids = set(permissions) - existing_ids
        if missing_ids:
            raise PermissionNotFoundException(
                f"Permissions with ids {missing_ids} do not exist."
            )

    async def bulk_link_permissions_to_role(
        self, role_id: int, permission_ids: list[int]
    ) -> None:
        self.db.query(RolePermissionAssociation).filter(
            RolePermissionAssociation.role_id == role_id
        ).delete()
        self.db.flush()
        new_associations = [
            RolePermissionAssociation(role_id=role_id, permission_id=permission_id)
            for permission_id in permission_ids
        ]
        self.db.bulk_save_objects(new_associations)
