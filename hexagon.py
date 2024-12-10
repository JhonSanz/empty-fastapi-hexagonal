HTTP_ACTIONS = ["create", "list", "retrieve", "update", "delete"]

INFRASTRUCTURE_WEB = """
from fastapi import APIRouter, Depends, Query, status
from typing import Annotated
from src.common.std_response import std_response, StandardResponse
from src.common.database_connection import get_db
from sqlalchemy.orm import Session

from src.__my_model__.application.handlers import (
    create_handler,
    retrieve_handler,
    list_handler,
    update_handler,
    delete_handler
)
from src.__my_model__.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase
)
from src.__my_model__.application.schemas import (
    __MY_MODEL__InDBBase,
    Create__MY_MODEL__Request,
    Update__MY_MODEL__Request,
    FilterParams,
)
from src.__my_model__.infrastructure.database import ORM__MY_MODEL__Repository
from src.__my_model__.application.service import __MY_MODEL__Service


router = APIRouter()

"""

http_actions_methods = []

for action in HTTP_ACTIONS:
    current = ""

    if action == "create":
        current += '@router.post("/create", response_model=StandardResponse[__MY_MODEL__InDBBase])'
    if action == "delete":
        current += '@router.delete("/{__my_model___id}/delete", response_model=StandardResponse[__MY_MODEL__InDBBase])'
    if action == "retrieve":
        current += '@router.get("/{__my_model___id}/retrieve", response_model=StandardResponse[__MY_MODEL__InDBBase])'
    if action == "list":
        current += '@router.get("/list", response_model=StandardResponse[list[__MY_MODEL__InDBBase]])'
    if action == "update":
        current += '@router.put("/{__my_model___id}/update", response_model=StandardResponse[__MY_MODEL__InDBBase])'

    if action in ["retrieve", "delete"]:
        current += f"""
async def {action}_endpoint(
    __my_model___id: int,
    database: Session = Depends(get_db)
):
        """

    if action == "create":
        current += f"""
async def {action}_endpoint(
    {action}___my_model___request: {action.capitalize()}__MY_MODEL__Request,
    database: Session = Depends(get_db)
):
        """

    if action == "list":
        current += f"""
async def {action}_endpoint(
    filter_params: Annotated[FilterParams, Query()],
    database: Session = Depends(get_db)
):
        """

    if action == "update":
        current += f"""
async def {action}_endpoint(
    __my_model___id: int,
    {action}___my_model___request: {action.capitalize()}__MY_MODEL__Request,
    database: Session = Depends(get_db)
):
        """

    current += f"""
    __my_model___repo = ORM__MY_MODEL__Repository(db=database)
    __my_model___service = __MY_MODEL__Service()
    {action}_use_case = {action.capitalize()}UseCase(
        __my_model___repository=__my_model___repo,
        __my_model___service=__my_model___service
    )
    """

    if action == "create":
        current += f"""
    result = {action}_handler(
        {action}___my_model___request={action}___my_model___request,
        {action}_use_case={action}_use_case
    )
    return std_response(data=result)
        """

    if action == "update":
        current += f"""
    result = {action}_handler(
        __my_model___id=__my_model___id,
        {action}___my_model___request={action}___my_model___request,
        {action}_use_case={action}_use_case
    )
    return std_response(data=result)
        """

    if action == "retrieve":
        current += f"""
    result = {action}_handler(
        __my_model___id=__my_model___id,
        {action}_use_case={action}_use_case
    )
    return std_response(data=result)
        """

    if action == "list":
        current += f"""
    result, count = {action}_handler(
        filter_params=filter_params,
        {action}_use_case={action}_use_case
    )
    return std_response(data=result, count=count)
        """

    if action == "delete":
        current += f"""
    result = {action}_handler(
        __my_model___id=__my_model___id,
        {action}_use_case={action}_use_case
    )
    return std_response(data=result)
        """

    http_actions_methods.append(current)

INFRASTRUCTURE_WEB += "\n\n".join(http_actions_methods)


INFRASTRUCTURE_DATABASE = """
from src.__my_model__.domain.repository import __MY_MODEL__Repository
from src.__my_model__.domain.models import __MY_MODEL__
from src.__my_model__.application.schemas import (
    __MY_MODEL__InDBBase,
    Create__MY_MODEL__Request,
    Update__MY_MODEL__Request,
    FilterParams,
)
from src.__my_model__.domain.exceptions import __MY_MODEL__NotFoundException 


class ORM__MY_MODEL__Repository(__MY_MODEL__Repository):
    def __init__(self, *, db):
        self.db = db

    async def get_by_id(self, *, id: int) -> __MY_MODEL__:
        existing___my_model__ = (
            self.db.query(__MY_MODEL__).filter(__MY_MODEL__.id == id).first()
        )
        if not existing___my_model__:
            raise __MY_MODEL__NotFoundException(f"__MY_MODEL__ {id} not found")
        return existing___my_model__

    async def get(self, *, filter_params: FilterParams) -> tuple[list[__MY_MODEL__], int]:
        filters_ = {}
        __my_model___query = (
            self.db.query(__MY_MODEL__).filter_by(**filters_).order_by(__MY_MODEL__.id.desc())
        )
        count = __my_model___query.count()
        __my_model__ = __my_model___query.offset(filter_params.skip).limit(filter_params.limit).all()
        return __my_model__, count

    async def create(self, *, data: Create__MY_MODEL__Request):
        __my_model___result = __MY_MODEL__(**data)
        self.db.add(__my_model___result)
        self.db.flush()
        self.db.refresh(__my_model___result)
        return __my_model___result

    async def update(self, *, id: int, data: Update__MY_MODEL__Request):
        __my_model___result = (
            self.db.query(__MY_MODEL__)
            .filter(__MY_MODEL__.id == id)
            .update(data, synchronize_session="fetch")
        )

        if __my_model___result == 0:
            raise __MY_MODEL__NotFoundException(f"__MY_MODEL__ with ID {id} not found")

        updated___my_model__ = (
            self.db.query(__MY_MODEL__).filter(__MY_MODEL__.id == id).first()
        )
        self.db.refresh(updated___my_model__)
        return updated___my_model__

    async def delete(self, *, id: int):
        # TODO:
        pass
"""


# ---


DOMAIN_SERVICE = f"""
from src.__my_model__.application.interfaces import __MY_MODEL__ServiceInterface

class __MY_MODEL__Service(__MY_MODEL__ServiceInterface):
    # TODO:
    def my_method(self, *, my_param: None) -> None: ...
"""


DOMAIN_REPOSITORY = f"""
from abc import ABC, abstractmethod
from src.__my_model__.domain.models import __MY_MODEL__


class __MY_MODEL__Repository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int) -> __MY_MODEL__: ...

    @abstractmethod
    async def get(self, *, id: int, filter_params) -> tuple[list[__MY_MODEL__], int]: ...

    @abstractmethod
    async def create(self, *, data): ...

    @abstractmethod
    async def update(self, *, id: int, data): ...

    @abstractmethod
    async def delete(self, *, id: int): ...
"""


DOMAIN_MODELS = """
# TODO: sqlalchemy models here

class __MY_MODEL__:
    # TODO:
    pass
"""


DOMAIN_EXCEPTIONS = """
from src.common.std_response import std_response, StandardResponse
from fastapi import Request, status


class __MY_MODEL__NotFoundException(Exception):
    pass

async def __my_model___not_found_handler(request: Request, exc: __MY_MODEL__NotFoundException):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg=str(exc),
        data=None,
    )

EXCEPTIONS___MY_MODEL___MAPPING = [
    (__my_model___not_found_handler, __MY_MODEL__NotFoundException),
]
"""


APPLICATION_SCHEMAS = """
from pydantic import BaseModel


class __MY_MODEL__InDBBase(BaseModel):
    # TODO:
    pass


class Create__MY_MODEL__Request(BaseModel):
    # TODO:
    pass

    
class Update__MY_MODEL__Request(BaseModel):
    # TODO:
    pass


class FilterParams(BaseModel):
    skip: int = 0
    limit: int = 10

"""


APPLICATION_HANDLERS = """
from src.__my_model__.application.use_cases import (
    CreateUseCase,
    RetrieveUseCase,
    ListUseCase,
    UpdateUseCase,
    DeleteUseCase
)
from src.__my_model__.application.schemas import (
    Create__MY_MODEL__Request,
    Update__MY_MODEL__Request,
    FilterParams,
)
from src.__my_model__.domain.models import __MY_MODEL__
"""

application_handlers_methods = []
for action in HTTP_ACTIONS:

    current = f"""
def {action}_handler(
    *,
"""

    if action == "create":
        current += f"""
    {action}___my_model___request: {action.capitalize()}__MY_MODEL__Request, 
    {action}_use_case: {action.capitalize()}UseCase
):
    data = {action}_use_case.execute(__my_model___request={action}___my_model___request)
    return data
        """

    if action == "update":
        current += f"""
    __my_model___id: int,
    {action}___my_model___request: {action.capitalize()}__MY_MODEL__Request, 
    {action}_use_case: {action.capitalize()}UseCase
):
    data = {action}_use_case.execute(
        __my_model___id=__my_model___id,
        __my_model___request={action}___my_model___request
    )
    return data
        """

    if action == "retrieve":
        current += f"""
    __my_model___id: int,
    {action}_use_case: {action.capitalize()}UseCase
):
    data = {action}_use_case.execute(__my_model___id=__my_model___id)
    return data
        """

    if action == "list":
        current += f"""
    filter_params: FilterParams,
    {action}_use_case: {action.capitalize()}UseCase
) -> tuple[list[__MY_MODEL__], int]:
    data, count = {action}_use_case.execute(filter_params=filter_params)
    return data, count
        """

    if action == "delete":
        current += f"""
    __my_model___id: int,
    {action}_use_case: {action.capitalize()}UseCase
):
    data = {action}_use_case.execute(__my_model___id=__my_model___id)
    return data
        """

    application_handlers_methods.append(current)

APPLICATION_HANDLERS += "\n".join(application_handlers_methods)


APPLICATION_INTERFACES = """
from abc import ABC, abstractmethod


class __MY_MODEL__ServiceInterface(ABC):
    @abstractmethod
    def my_method(self, my_param: None) -> None: ...
"""

APPLICATION_WEB_CASES = [
    """
from .create import CreateUseCase
from .delete import DeleteUseCase
from .retrieve import RetrieveUseCase
from .list import ListUseCase
from .update import UpdateUseCase
    """
]

application_web_cases_actions = []
for action in HTTP_ACTIONS:
    current_action = f"""
from src.__my_model__.domain.repository import __MY_MODEL__Repository
from src.__my_model__.domain.exceptions import __MY_MODEL__NotFoundException
from src.__my_model__.domain.models import __MY_MODEL__
from src.__my_model__.application.interfaces import __MY_MODEL__ServiceInterface
    """

    if action in ["create", "update"]:
        current_action += f"""
from src.__my_model__.application.schemas import {action.capitalize()}__MY_MODEL__Request
    """
        
    if action == "list":
        current_action += f"""
from src.__my_model__.application.schemas import FilterParams
    """

    current_action += f"""
class {action.capitalize()}UseCase:
    def __init__(
        self, *, __my_model___repository: __MY_MODEL__Repository, __my_model___service: __MY_MODEL__ServiceInterface
    ):
        self.__my_model___repository = __my_model___repository
        self.__my_model___service = __my_model___service
    """

    if action == "create":
        current_action += f"""
    def execute(self, *, __my_model___request: {action.capitalize()}__MY_MODEL__Request) -> None:
        # TODO: your logic here
        self.store_repository.create(data=__my_model___request)
        return
    """

    if action == "update":
        current_action += f"""
    def execute(self, *, __my_model___id: int, __my_model___request: {action.capitalize()}__MY_MODEL__Request) -> None:
        # TODO: your logic here
        self.store_repository.update(id=__my_model___id, data=__my_model___request)
        return
    """

    if action == "list":
        current_action += f"""
    def execute(self, *, filter_params: FilterParams) -> tuple[list[__MY_MODEL__], int]:
        # TODO: your logic here
        data, count = self.store_repository.get(filter_params=filter_params)
        return data, count
    """

    if action in "retrieve":
        current_action += f"""
    def execute(self, *,__my_model___id: int) -> __MY_MODEL__:
        # TODO: your logic here
        data = self.store_repository.get_by_id(id=__my_model___id)
        return data
    """
        
    if action in "delete":
        current_action += f"""
    def execute(self, *, __my_model___id: int) -> None:
        # TODO: your logic here
        self.store_repository.delete(id=__my_model___id)
        return
    """

    application_web_cases_actions.append(current_action)

APPLICATION_WEB_CASES += application_web_cases_actions

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
            (f"src/{base_dir}/application/service.py", DOMAIN_SERVICE),
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
