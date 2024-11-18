INFRASTRUCTURE_WEB = """
from src.__my_model__.application.handlers import (
    create_handler,
    retrieve_handler,
    update_handler,
    delete_handler
)
from src.__my_model__.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    UpdateUseCase,
    DeleteUseCase
)
from src.__my_model__.application.schemas import (
    CreateRequest,
    RetrieveRequest,
    UpdateRequest,
    DeleteRequest
)
from src.__my_model__.infrastructure.database import ORM__MY_MODEL__Repository
from src.__my_model__.domain.service import __MY_MODEL__Service
"""

methods = [
    f"""
    def {action}_endpoint():
        request = {action.capitalize()}Request
        __my_model__repo = ORM__MY_MODEL__Repository(db=db_session)
        __my_model__service = __MY_MODEL__Service()
        login_use_case = {action.capitalize()}UseCase(
            __my_model__repository=__my_model__repo,
            __my_model__service=__my_model__service
        )
        return login_handler(login_request, login_use_case=login_use_case)
    """
    for action in ("create", "retrieve", "update", "delete")
]
INFRASTRUCTURE_WEB += "\n\n".join(methods)


INFRASTRUCTURE_DATABASE = """
from src.__my_model__.domain.repository import __MY_MODEL__Repository
from src.__my_model__.domain.models import __MY_MODEL__

class ORM__MY_MODEL__Repository(__MY_MODEL__Repository):
    async def get_by_id(self, *, id: int) -> __MY_MODEL__:
        pass

    async def get(self, *, id: int) -> list[__MY_MODEL__]:
        pass

    async def create(self, *, data):
        pass

    async def update(self, *, id: int, data):
        pass

    async def delete(self, *, id: int):
        pass
"""


# ---


DOMAIN_SERVICE = f"""
from src.__my_model__.application.interfaces import __MY_MODEL__ServiceInterface

class __MY_MODEL__Service(__MY_MODEL__ServiceInterface):
    def my_method(self, *, my_param: None) -> None: ...
"""


DOMAIN_REPOSITORY = f"""
from abc import ABC, abstractmethod
from src.__my_model__.domain.models import __MY_MODEL__


class __MY_MODEL__Repository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int) -> __MY_MODEL__: ...

    @abstractmethod
    async def get(self, *, id: int) -> list[__MY_MODEL__]: ...

    @abstractmethod
    async def create(self, *, data): ...

    @abstractmethod
    async def update(self, *, id: int, data): ...

    @abstractmethod
    async def delete(self, *, id: int): ...
"""


DOMAIN_MODELS = "# sqlalchemy models here"


DOMAIN_EXCEPTIONS = """
class __MY_MODEL__NotFoundException(Exception):
    pass
"""


# ---


APPLICATION_SCHEMAS = """
from pydantic import BaseModel


class CreateRequest(BaseModel):
    pass

    
class RetrieveRequest(BaseModel):
    pass

    
class UpdateRequest(BaseModel):
    pass

    
class DeleteRequest(BaseModel):
    pass
"""


APPLICATION_HANDLERS = """
from src.__my_model__.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    UpdateUseCase,
    DeleteUseCase
)
from src.__my_model__.application.schemas import (
    CreateRequest,
    RetrieveRequest,
    UpdateRequest,
    DeleteRequest
)
"""

application_handlers_methods = [
    f"""
    def {action}_handler(
        {action}_request: {action.capitalize()}Request, 
        {action}_use_case: {action.capitalize()}UseCase
    ):
        data = {action}_use_case.execute({action}_request={action}_request)
        return std_response(data=data)
    """
    for action in ("create", "retrieve", "update", "delete")
]
APPLICATION_HANDLERS += "\n\n".join(application_handlers_methods)


APPLICATION_INTERFACES = """
from abc import ABC, abstractmethod


class __MY_MODEL__ServiceInterface(ABC):
    @abstractmethod
    def my_method(self, my_param: None) -> None: ...
        pass
"""

