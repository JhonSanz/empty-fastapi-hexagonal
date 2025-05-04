from abc import ABC, abstractmethod


class UserServiceInterface(ABC):
    @abstractmethod
    def user_can_be_created(self, *, user_request) -> None: ...

    @abstractmethod
    def check_password_format(self, *, password): ...

    @abstractmethod
    def hash_password(self, *, password): ...

    @abstractmethod
    def verify_password(self, *, password, hashed_password): ...

    @abstractmethod
    def user_by_email_exists(self, *, email) -> bool: ...

    @abstractmethod
    def check_and_link_roles(self, *, user_id, roles) -> None: ...

    @abstractmethod
    async def generate_random_string(self, *, length) -> str: ...
