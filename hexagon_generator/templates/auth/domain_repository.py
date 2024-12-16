DOMAIN_REPOSITORY_TEMPLATE = """from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class AuthRepository(ABC):
    @abstractmethod
    async def get_user_by_identification(self, db: Session, identification: str): ...

"""