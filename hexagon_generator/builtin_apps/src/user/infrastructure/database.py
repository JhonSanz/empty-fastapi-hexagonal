from sqlalchemy.orm import joinedload, load_only
from src.user.domain.repository import UserRepository
from src.user.domain.models import User, UserRoleAssociation
from src.user.application.schemas import (
    UserInDBBase,
    CreateUserRequest,
    UpdateUserRequest,
    FilterParams,
)
from src.user.domain.exceptions import UserNotFoundException
from src.role.infrastructure.database import ORMRoleRepository
from src.role.domain.models import Role


class ORMUserRepository(UserRepository):
    def __init__(self, *, db, role_repository: ORMRoleRepository = None):
        self.db = db
        self.role_repository = role_repository

    async def get_by_id(self, *, id: int, filter_params: FilterParams) -> User:
        existing_user = self.db.query(User).filter(User.id == id)
        if filter_params.show_roles:
            existing_user = existing_user.options(joinedload(User.roles))

        existing_user = existing_user.first()
        if not existing_user:
            raise UserNotFoundException(f"User {id} not found")
        return existing_user

    async def get(self, *, filter_params: FilterParams) -> tuple[list[User], int]:
        filters_ = filter_params.model_dump(
            exclude={"show_roles", "skip", "limit"}, exclude_none=True
        )
        user_query = self.db.query(User).filter_by(**filters_).order_by(User.id.desc())

        if filter_params.show_roles:
            user_query = user_query.options(joinedload(User.roles))

        count = user_query.count()
        user = user_query.offset(filter_params.skip).limit(filter_params.limit).all()
        return user, count

    async def create(self, *, data: CreateUserRequest) -> User:
        data_ = data.model_dump(exclude={"roles"})
        user_result = User(**data_)
        self.db.add(user_result)
        self.db.flush()
        self.db.refresh(user_result)
        return user_result

    async def update(self, *, id: int, data: UpdateUserRequest):
        data_ = data.model_dump(exclude_none=True, exclude={"roles"})
        user_result = (
            self.db.query(User)
            .filter(User.id == id)
            .update(data_, synchronize_session="fetch")
        )

        if user_result == 0:
            raise UserNotFoundException(f"User with ID {id} not found")

        updated_user = self.db.query(User).filter(User.id == id).first()
        self.db.refresh(updated_user)
        return updated_user

    async def delete(self, *, id: int):
        existing_user = self.db.query(User).filter(User.id == id).first()
        if not existing_user:
            raise UserNotFoundException(f"User with ID {id} not found")
        self.db.query(UserRoleAssociation).filter(
            UserRoleAssociation.user_id == id
        ).delete()
        self.db.delete(existing_user)
        self.db.flush()

    async def check_roles_exist(self, *, roles: list[int]):
        await self.role_repository.check_roles_exist(roles=roles)

    async def bulk_link_roles_to_user(self, *, user_id: int, roles_ids: list[int]):
        self.db.query(UserRoleAssociation).filter(
            UserRoleAssociation.user_id == user_id
        ).delete()
        self.db.flush()
        new_associations = [
            UserRoleAssociation(role_id=role_id, user_id=user_id)
            for role_id in roles_ids
        ]
        self.db.bulk_save_objects(new_associations)
