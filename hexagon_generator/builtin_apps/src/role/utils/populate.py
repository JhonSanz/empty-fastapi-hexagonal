from src.common.database_connection import Base, SessionLocal
from src.common.utils.models_import import models_import
from src.role.domain.models import Permission, Role, RolePermissionAssociation

models_import()

black_listed_tables = ["Permission", "RolePermissionAssociation"]
actions = ["create", "update", "delete", "get", "list"]
tables = [mapper.class_.__name__ for mapper in Base.registry.mappers]
permissions_list = [
    f"{table.lower()}.{action}"
    for table in tables
    for action in actions
    if not table in black_listed_tables
]

session = SessionLocal()

permissions = []
for permission_name in permissions_list:
    existing_permission = (
        session.query(Permission).filter_by(name=permission_name).first()
    )
    if not existing_permission:
        permission = Permission(name=permission_name)
        session.add(permission)
        session.flush()
        permissions.append(permission)
    else:
        permissions.append(existing_permission)

superuser_role = session.query(Role).filter_by(name="superuser").first()
if not superuser_role:
    superuser_role = Role(name="superuser")
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


try:
    session.commit()
    print("Permisos añadidos exitosamente.")
except Exception as e:
    session.rollback()
    print(f"Error al añadir permisos: {e}")
finally:
    session.close()
