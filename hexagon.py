HTTP_ACTIONS = ["create", "retrieve", "update", "delete"]

INFRASTRUCTURE_WEB = """
from fastapi import APIRouter, Depends, Query, status
from src.common.std_response import std_response, StandardResponse
from src.common.database_connection import get_db
from sqlalchemy.orm import Session

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
    __MY__MODEL__InDBBase,
    Create__MY_MODEL__Request,
    Retrieve__MY_MODEL__Request,
    Update__MY_MODEL__Request,
    Delete__MY_MODEL__Request
)
from src.__my_model__.infrastructure.database import ORM__MY_MODEL__Repository
from src.__my_model__.domain.service import __MY_MODEL__Service


router = APIRouter()

"""

http_actions_methods = []

for action in HTTP_ACTIONS:
    current = ""

    if action == "create":
        current += '@router.post("/create", response_model=StandardResponse[__MY__MODEL__InDBBase])'
    if action == "delete":
        current += '@router.delete("/{__my_model___id}/delete", response_model=StandardResponse[__MY__MODEL__InDBBase])'
    if action == "retrieve":
        current += '@router.get("/{__my_model___id}/retrieve", response_model=StandardResponse[__MY__MODEL__InDBBase])'
    if action == "update":
        current += '@router.put("/{__my_model___id}/retrieve", response_model=StandardResponse[__MY__MODEL__InDBBase])'
    
    f"""
async def {action}_endpoint(database: Session = Depends(get_db)):
    {action}___my_model___request = {action.capitalize()}__MY_MODEL__Request
    __my_model___repo = ORM__MY_MODEL__Repository(db=db_session)
    __my_model___service = __MY_MODEL__Service()
    {action}_use_case = {action.capitalize()}UseCase(
        __my_model___repository=__my_model___repo,
        __my_model___service=__my_model___service
    )
    result = {action}_handler(
        {action}___my_model___request={action}___my_model___request,
        {action}_use_case={action}_use_case
    )
    return std_response(data=result)
    """
    http_actions_methods.append(current)

INFRASTRUCTURE_WEB += "\n\n".join(http_actions_methods)


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


DOMAIN_MODELS = "# TODO: sqlalchemy models here"


DOMAIN_EXCEPTIONS = """
from src.common.std_response import std_response, StandardResponse


class __MY_MODEL__NotFoundException(Exception):
    pass

async def __my__model___not_found_handler(request: Request, exc: __MY_MODEL__NotFoundException):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg=str(exc),
        data=None,
    )

EXCEPTIONS___MY_MODEL___MAPPING = [
    (__my__model___not_found_handler, __MY_MODEL__NotFoundException),
]
"""


APPLICATION_SCHEMAS = """
from pydantic import BaseModel


class __MY__MODEL__InDBBase(BaseModel):
    pass


class Create__MY_MODEL__Request(BaseModel):
    pass

    
class Retrieve__MY_MODEL__Request(BaseModel):
    pass

    
class Update__MY_MODEL__Request(BaseModel):
    pass

    
class Delete__MY_MODEL__Request(BaseModel):
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
    Create__MY_MODEL__Request,
    Retrieve__MY_MODEL__Request,
    Update__MY_MODEL__Request,
    Delete__MY_MODEL__Request
)
"""

application_handlers_methods = [
    f"""
def {action}_handler(
    {action}___my_model___request: {action.capitalize()}__MY_MODEL__Request, 
    {action}_use_case: {action.capitalize()}UseCase
):
    data = {action}_use_case.execute({action}___my_model___request={action}___my_model___request)
    return data
    """
    for action in HTTP_ACTIONS
]
APPLICATION_HANDLERS += "\n\n".join(application_handlers_methods)


APPLICATION_INTERFACES = """
from abc import ABC, abstractmethod


class __MY_MODEL__ServiceInterface(ABC):
    @abstractmethod
    def my_method(self, my_param: None) -> None:
        pass
"""

APPLICATION_WEB_CASES = (
    [
        """
from .create import CreateUseCase
from .delete import DeleteUseCase
from .retrieve import RetrieveUseCase
from .update import UpdateUseCase
    """
    ]
    + [
        f"""
from src.__my_model__.domain.repository import __MY_MODEL__Repository
from src.__my_model__.domain.exceptions import __MY_MODEL__NotFoundException
from src.__my_model__.domain.models import __MY_MODEL__
from src.__my_model__.application.interfaces import __MY_MODEL__ServiceInterface


class {action.capitalize()}UseCase:
    def __init__(
        self, *, __my_model___repository: __MY_MODEL__Repository, __my_model___service: __MY_MODEL__ServiceInterface
    ):
        self.__my_model___repository = __my_model___repository
        self.__my_model___service = __my_model___service

    def execute(self, *, my_param: None) -> None:
        # TODO: your logic here
        return
    """
        for action in HTTP_ACTIONS
    ]
)


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
        self.template = self.template.replace("__my_model__", self.snake)

    def save_file_to_path(self):
        if os.path.exists(self.filepath):
            print(f"El archivo {self.filepath} ya existe. No se sobrescribirá.")
        else:
            with open(self.filepath, "w") as file:
                file.write(self.template)
            print(f"Archivo {self.filepath} creado exitosamente.")

    @staticmethod
    def create_dir(dir_name: str):
        try:
            os.mkdir(dir_name)
            print(f"Directory '{dir_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{dir_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{dir_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")


class ModelGenerator:
    def __init__(self, model_label, snake):
        self.model_label: str = model_label
        self.snake: str = snake

    def create_mandatory_dirs(self):
        base_dir = self.model_label.lower()
        dirs = [
            f"src/{base_dir}",
            f"src/{base_dir}/application",
            f"src/{base_dir}/domain",
            f"src/{base_dir}/infrastructure",
            f"src/{base_dir}/application/use_cases",
        ]
        for dir_ in dirs:
            CodeGenerator.create_dir(dir_name=dir_)

    def create_use_cases(self):
        base_dir = self.model_label.lower()
        for index, (use_case, action) in enumerate(
            zip(APPLICATION_WEB_CASES, [""] + HTTP_ACTIONS)
        ):
            filepath = f"src/{base_dir}/application/use_cases/{action}.py"
            if index == 0:
                filepath = f"src/{base_dir}/application/use_cases/__init__.py"
            code_gen = CodeGenerator(
                model_label=self.model_label,
                snake=self.snake,
                filepath=filepath,
                template=use_case,
            )
            code_gen.replace_model_name()
            code_gen.replace_snake_name()
            code_gen.save_file_to_path()

    def run(self):
        self.create_mandatory_dirs()
        base_dir = self.model_label.lower()
        routes = [
            (f"src/{base_dir}/infrastructure/web.py", INFRASTRUCTURE_WEB),
            (f"src/{base_dir}/infrastructure/database.py", INFRASTRUCTURE_DATABASE),
            (f"src/{base_dir}/domain/exceptions.py", DOMAIN_EXCEPTIONS),
            (f"src/{base_dir}/domain/models.py", DOMAIN_MODELS),
            (f"src/{base_dir}/domain/repository.py", DOMAIN_REPOSITORY),
            (f"src/{base_dir}/domain/service.py", DOMAIN_SERVICE),
            (f"src/{base_dir}/application/schemas.py", APPLICATION_SCHEMAS),
            (f"src/{base_dir}/application/handlers.py", APPLICATION_HANDLERS),
            (f"src/{base_dir}/application/interfaces.py", APPLICATION_INTERFACES),
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
        self.create_use_cases()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generador de archivos hexagonales para CRUD."
    )
    parser.add_argument("model_name", type=str, help="Nombre del modelo (PascalCase).")
    parser.add_argument("snake_name", type=str, help="Nombre del modelo (snake_case).")

    args = parser.parse_args()

    ModelGenerator(
        model_label=args.model_name,
        snake=args.snake_name,
    ).run()
