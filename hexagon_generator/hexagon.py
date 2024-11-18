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

import os
import argparse


class CodeGenerator:
    def __init__(self, model_label, snake, template, filepath):
        self.template = template
        self.filepath = filepath
        self.model_label = model_label
        self.snake = snake

    def replace_model_name(self):
        self.template = self.template.replace("__MY_MODEL__", self.model_label)

    def replace_snake_name(self):
        self.template = self.template.replace("_my_model_", self.snake)

    def save_file_to_path(self):
        if os.path.exists(self.filepath):
            print(f"El archivo {self.filepath} ya existe. No se sobrescribirá.")
        else:
            with open(self.filepath, "w") as file:
                file.write(self.template)
            print(f"Archivo {self.filepath} creado exitosamente.")


class ModelGenerator:
    def __init__(self, model_label, snake, filename):
        self.model_label: str = model_label
        self.snake: str = snake
        self.filename: str = filename

    def create_dir(self, dir_name: str):
        try:
            os.mkdir(dir_name)
            print(f"Directory '{dir_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{dir_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{dir_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_mandatory_dirs(self):
        base_dir = self.model_label.lower()
        self.create_dir(dir_name=base_dir)
        self.create_dir(dir_name=f"{base_dir}/application")
        self.create_dir(dir_name=f"{base_dir}/domain")
        self.create_dir(dir_name=f"{base_dir}/infrastructure")

    def run(self):
        self.create_mandatory_dirs()
        base_dir = self.model_label.lower()
        routes = [
            (f"{base_dir}/infrastructure/web.py", INFRASTRUCTURE_WEB),
            (f"{base_dir}/infrastructure/database.py", INFRASTRUCTURE_DATABASE),
            (f"{base_dir}/domain/exceptions.py", DOMAIN_EXCEPTIONS),
            (f"{base_dir}/domain/models.py", DOMAIN_MODELS),
            (f"{base_dir}/domain/repository.py", DOMAIN_REPOSITORY),
            (f"{base_dir}/domain/service.py", DOMAIN_SERVICE),
            (f"{base_dir}/application/schemas.py", APPLICATION_SCHEMAS),
            (f"{base_dir}/application/handlers.py", APPLICATION_HANDLERS),
            (f"{base_dir}/application/interfaces.py", APPLICATION_INTERFACES),
        ]
        for route in routes:
            code_gen = CodeGenerator(
                model_label=self.model_label,
                snake=self.snake,
                filepath=route[0],
                template=route[1],
            )
            code_gen.replace_model_name()
            code_gen.replace_snake_name()
            code_gen.save_file_to_path()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generador de archivos hexagonales para CRUD."
    )
    parser.add_argument("model_name", type=str, help="Nombre del modelo (PascalCase).")
    parser.add_argument("snake_name", type=str, help="Nombre del modelo (snake_case).")

    args = parser.parse_args()

    ModelGenerator(
        filename=args.filename,
        model_label=args.model_name,
        snake=args.snake_name,
    ).run()
