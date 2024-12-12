import os
import argparse
from jinja2 import Template

from hexagon_generator.templates.application_handlers import (
    APPLICATION_HANDLERS_TEMPLATE,
)
from hexagon_generator.templates.application_interfaces import (
    APPLICATION_INTERFACES_TEMPLATE,
)
from hexagon_generator.templates.application_schemas import APPLICATION_SCHEMAS_TEMPLATE
from hexagon_generator.templates.application_service import APPLICATION_SERVICE_TEMPLATE
from hexagon_generator.templates.application_web_cases import (
    APPLICATION_WEB_CASE_TEMPLATE,
    APPLICATION_WEB_CASE_TEMPLATE_INIT,
)
from hexagon_generator.templates.domain_exceptions import DOMAIN_EXCEPTIONS_TEMPLATE
from hexagon_generator.templates.domain_models import DOMAIN_MODELS_TEMPLATE
from hexagon_generator.templates.domain_repository import DOMAIN_REPOSITORY_TEMPLATE
from hexagon_generator.templates.infrastructure_database import (
    INFRASTRUCTURE_DATABASE_TEMPLATE,
)
from hexagon_generator.templates.infrastructure_web import INFRASTRUCTURE_WEB_TEMPLATE

HTTP_ACTIONS = ["create", "list", "retrieve", "update", "delete"]


class CodeGenerator:
    def __init__(self, *, pascal_case, snake_case, filepath):
        self.template = None
        self.filepath = filepath
        self.pascal_case = pascal_case
        self.snake_case = snake_case

    def render_template(self, *, template_imported: str):
        template = Template(template_imported)
        self.template = template.render(
            model_snake_case=self.snake_case,
            model_pascal_case=self.pascal_case,
            actions=HTTP_ACTIONS,
        )

    def save_file_to_path(self):
        if os.path.exists(self.filepath):
            print(f"El archivo {self.filepath} ya existe. No se sobrescribirá.")
        else:
            with open(self.filepath, "w") as file:
                file.write(self.template)
            print(f"Archivo {self.filepath} creado exitosamente.")

    @staticmethod
    def create_dir(*, dir_name: str):
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
    def __init__(self, pascal_case, snake_case):
        self.pascal_case: str = pascal_case
        self.snake_case: str = snake_case

    def create_mandatory_dirs(self):
        base_dir = self.pascal_case.lower()
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
        base_dir = self.pascal_case.lower()

        code_gen = CodeGenerator(
            pascal_case=self.pascal_case,
            snake_case=self.snake_case,
            filepath=f"src/{base_dir}/application/use_cases/__init__.py",
        )
        code_gen.render_template(template_imported=APPLICATION_WEB_CASE_TEMPLATE_INIT)
        code_gen.save_file_to_path()

        template = Template(APPLICATION_WEB_CASE_TEMPLATE)
        application_web_cases_actions = []
        for action in HTTP_ACTIONS:
            rendered_case = template.render(
                model_snake_case=self.snake_case,
                model_pascal_case=self.pascal_case,
                action=action,
            )
            application_web_cases_actions.append(rendered_case)

        for template, action in zip(application_web_cases_actions, HTTP_ACTIONS):
            filepath = f"src/{base_dir}/application/use_cases/{action}.py"
            code_gen = CodeGenerator(
                pascal_case=self.pascal_case,
                snake_case=self.snake_case,
                filepath=filepath,
            )
            code_gen.render_template(template_imported=template)
            code_gen.save_file_to_path()

    def run(self):
        self.create_mandatory_dirs()
        base_dir = self.pascal_case.lower()
        routes = [
            (f"src/{base_dir}/infrastructure/web.py", INFRASTRUCTURE_WEB_TEMPLATE),
            (
                f"src/{base_dir}/infrastructure/database.py",
                INFRASTRUCTURE_DATABASE_TEMPLATE,
            ),
            (f"src/{base_dir}/domain/exceptions.py", DOMAIN_EXCEPTIONS_TEMPLATE),
            (f"src/{base_dir}/domain/models.py", DOMAIN_MODELS_TEMPLATE),
            (f"src/{base_dir}/domain/repository.py", DOMAIN_REPOSITORY_TEMPLATE),
            (f"src/{base_dir}/application/service.py", APPLICATION_SERVICE_TEMPLATE),
            (f"src/{base_dir}/application/schemas.py", APPLICATION_SCHEMAS_TEMPLATE),
            (f"src/{base_dir}/application/handlers.py", APPLICATION_HANDLERS_TEMPLATE),
            (
                f"src/{base_dir}/application/interfaces.py",
                APPLICATION_INTERFACES_TEMPLATE,
            ),
        ]
        for route in routes:
            code_gen = CodeGenerator(
                pascal_case=self.pascal_case,
                snake_case=self.snake_case,
                filepath=route[0],
            )
            code_gen.render_template(template_imported=route[1])
            code_gen.save_file_to_path()
        self.create_use_cases()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generador de archivos hexagonales para CRUD."
    )
    parser.add_argument("pascal_case", type=str, help="Nombre del modelo (PascalCase).")
    parser.add_argument("snake_name", type=str, help="Nombre del modelo (snake_case).")

    args = parser.parse_args()

    ModelGenerator(
        pascal_case=args.pascal_case,
        snake_case=args.snake_name,
    ).run()
