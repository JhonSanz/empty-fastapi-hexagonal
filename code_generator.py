import os
import argparse
from jinja2 import Template
import shutil
import os


from hexagon_generator.templates.crud.application_web_cases import (
    APPLICATION_WEB_CASE_TEMPLATE,
    APPLICATION_WEB_CASE_TEMPLATE_INIT,
)
from hexagon_generator.templates.crud.routes import (
    routes as crud_routes,
    dirs as crud_dirs,
)

HTTP_ACTIONS = ["create", "list", "retrieve", "update", "delete"]


class CodeGenerator:
    def __init__(self, *, pascal_case, snake_case, filepath=None):
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
    def __init__(
        self, pascal_case, snake_case, routes, dirs, actions, use_cases_init, use_cases
    ):
        self.pascal_case: str = pascal_case
        self.snake_case: str = snake_case
        self.routes = routes
        self.dirs = dirs
        self.actions = actions
        self.use_cases_init = use_cases_init
        self.use_cases = use_cases
        self.code_generator = None
        self.base_dir = None

    def create_mandatory_dirs(self):
        for dir_ in self.dirs:
            CodeGenerator.create_dir(dir_name=f"src/{self.base_dir}/{dir_}")

    def create_use_cases(self):
        filepath = f"src/{self.base_dir}/application/use_cases/__init__.py"
        self.code_generator.filepath = filepath
        self.code_generator.render_template(template_imported=self.use_cases_init)
        self.code_generator.save_file_to_path()

        template = Template(self.use_cases)
        application_web_cases_actions = []
        for action in self.actions:
            rendered_case = template.render(
                model_snake_case=self.snake_case,
                model_pascal_case=self.pascal_case,
                action=action,
            )
            application_web_cases_actions.append(rendered_case)

        for template, action in zip(application_web_cases_actions, self.actions):
            filepath = f"src/{self.base_dir}/application/use_cases/{action}.py"
            self.code_generator.filepath = filepath
            self.code_generator.render_template(template_imported=template)
            self.code_generator.save_file_to_path()

    def run(self):
        self.base_dir = self.pascal_case.lower()
        self.code_generator = CodeGenerator(
            pascal_case=self.pascal_case,
            snake_case=self.snake_case,
        )
        self.create_mandatory_dirs()
        for route in self.routes:
            code_gen = CodeGenerator(
                pascal_case=self.pascal_case,
                snake_case=self.snake_case,
                filepath=f"src/{self.base_dir}/{route[0]}",
            )
            code_gen.render_template(template_imported=route[1])
            code_gen.save_file_to_path()
        self.create_use_cases()


def copy_builtin_apps(*, app: str):
    source_dir_full = f"hexagon_generator/builtin_apps/src/{app}"
    destination_dir = f"src/{app}"

    # Si el directorio 'src' ya existe no hacemos nada
    if os.path.exists(destination_dir):
        print("Directorio 'src' ya existe.")
        return

    try:
        shutil.copytree(source_dir_full, destination_dir)
        print(f"Directorio copiado de {source_dir_full} a {destination_dir}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generador de archivos hexagonales para CRUD."
    )
    parser.add_argument("type", type=str, help="Tipo de codigo generado [auth, crud]")
    parser.add_argument(
        "pascal_case", type=str, nargs="?", help="Nombre del modelo (PascalCase)."
    )
    parser.add_argument(
        "snake_name", type=str, nargs="?", help="Nombre del modelo (snake_case)."
    )

    args = parser.parse_args()

    if args.type == "crud":
        if not args.pascal_case or not args.snake_name:
            parser.error(
                "Para 'crud', los argumentos 'pascal_case' y 'snake_name' son obligatorios."
            )
        ModelGenerator(
            pascal_case=args.pascal_case,
            snake_case=args.snake_name,
            dirs=crud_dirs,
            routes=crud_routes,
            actions=HTTP_ACTIONS,
            use_cases_init=APPLICATION_WEB_CASE_TEMPLATE_INIT,
            use_cases=APPLICATION_WEB_CASE_TEMPLATE,
        ).run()
    elif args.type in ["auth", "role", "user"]:
        copy_builtin_apps(app=args.type)
    else:
        parser.error(f"Tipo desconocido: {args.type}")
