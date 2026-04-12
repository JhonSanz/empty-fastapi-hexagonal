import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.common.database_connection import Base
from src.common.loggin_config import setup_logger
from src.common.utils.models_import import models_import
from src.role.infrastructure.models import PermissionORM, RoleORM, RolePermissionAssociation

logger = setup_logger()
models_import()

# Populate uses a sync engine since it runs as a standalone script
DATABASE_URL = os.getenv("DATABASE_URL")
sync_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
sync_engine = create_engine(sync_url)
SyncSession = sessionmaker(bind=sync_engine)

black_listed_tables = ["PermissionORM", "RolePermissionAssociation", "UserRoleAssociation"]
actions = ["create", "update", "delete", "get", "list"]
tables = [mapper.class_.__name__ for mapper in Base.registry.mappers]
permissions_list = [
    f"{table.lower().replace('orm', '')}.{action}"
    for table in tables
    for action in actions
    if table not in black_listed_tables
]

session = SyncSession()

permissions = []
for permission_name in permissions_list:
    existing_permission = (
        session.query(PermissionORM).filter_by(name=permission_name).first()
    )
    if not existing_permission:
        permission = PermissionORM(name=permission_name)
        session.add(permission)
        session.flush()
        permissions.append(permission)
    else:
        permissions.append(existing_permission)

superuser_role = session.query(RoleORM).filter_by(name="superuser").first()
if not superuser_role:
    superuser_role = RoleORM(name="superuser")
    session.add(superuser_role)
    session.flush()

for permission in permissions:
    existing_association = (
        session.query(RolePermissionAssociation)
        .filter_by(role_id=superuser_role.id, permission_id=permission.id)
        .first()
    )
    if not existing_association:
        association = RolePermissionAssociation(
            role_id=superuser_role.id, permission_id=permission.id
        )
        session.add(association)

session.commit()
session.close()
