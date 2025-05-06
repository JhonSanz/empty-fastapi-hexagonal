from jinja2 import Template

from hexagon_generator.core.code_gen import CodeGenerator
from hexagon_generator.core.constant import TARGET_ROOT


class ModelGenerator:
    def __init__(
        self,
        *,
        pascal_case,
        snake_case,
        routes,
        dirs,
        actions,
        use_cases_init,
        use_cases,
        code_generator,
    ):
        self.pascal_case: str = pascal_case
        self.snake_case: str = snake_case
        self.routes = routes
        self.dirs = dirs
        self.actions = actions
        self.use_cases_init = use_cases_init
        self.use_cases = use_cases
        self.code_generator: CodeGenerator = code_generator
        self.base_dir = None

    def create_mandatory_dirs(self):
        for dir_ in self.dirs:
            self.code_generator.create_dir(
                dir_name=f"{TARGET_ROOT}/src/{self.base_dir}/{dir_}"
            )

            if dir_ == "application/use_cases":
                continue

            self.code_generator.filepath = (
                f"{TARGET_ROOT}/src/{self.base_dir}/{dir_}/__init__.py"
            )
            self.code_generator.template = ""
            self.code_generator.save_file_to_path()

    def create_use_cases(self):
        filepath = (
            f"{TARGET_ROOT}/src/{self.base_dir}/application/use_cases/__init__.py"
        )
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
            filepath = (
                f"{TARGET_ROOT}/src/{self.base_dir}/application/use_cases/{action}.py"
            )
            self.code_generator.filepath = filepath
            self.code_generator.render_template(template_imported=template)
            self.code_generator.save_file_to_path()

    def create_routes(self):
        for route in self.routes:
            filepath = f"{TARGET_ROOT}/src/{self.base_dir}/{route[0]}"
            self.code_generator.filepath = filepath
            self.code_generator.render_template(template_imported=route[1])
            self.code_generator.save_file_to_path()

    def run(self):
        self.base_dir = self.pascal_case.lower()
        self.create_mandatory_dirs()
        self.create_routes()
        self.create_use_cases()
