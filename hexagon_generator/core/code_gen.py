import os
from jinja2 import Template
import os


class CodeGenerator:
    def __init__(self, *, pascal_case, snake_case, HTTP_ACTIONS=None, filepath=None):
        self.template = None
        self.filepath = filepath
        self.pascal_case = pascal_case
        self.snake_case = snake_case
        self.HTTP_ACTIONS = HTTP_ACTIONS

    def render_template(self, *, template_imported: str):
        template = Template(template_imported)
        self.template = template.render(
            model_snake_case=self.snake_case,
            model_pascal_case=self.pascal_case,
            actions=self.HTTP_ACTIONS,
        )

    def save_file_to_path(self):
        if os.path.exists(self.filepath):
            print(f"File {self.filepath} already exists. Won't be overritten.")
        else:
            with open(self.filepath, "w") as file:
                file.write(self.template)
            print(f"File {self.filepath} created successfully.")

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
