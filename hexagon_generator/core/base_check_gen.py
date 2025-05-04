from hexagon_generator.core.builtin_gen import BuiltInGenerator


class BaseDirsGenerator:
    MANDATORY_DIRS = [
        "env_vars",
        "src/alembic",
        "src/common",
    ]

    MANDATORY_FILES = [
        "src/__init__.py",
        "src/main.py",
        "src/config.py",
        ".env",
        ".gitignore",
        "alembic.ini",
        "docker-compose.yml",
        "dockerfile",
        "init.sh",
        "requirements.txt",
        "readme.md",
    ]

    def __init__(self, builtin_gen: BuiltInGenerator):
        self.builtin_gen = builtin_gen

    def create_mandatory_dirs(self):
        for path in self.MANDATORY_DIRS:
            self.builtin_gen.copy_builtin_apps(path_source=path, path_target=path)

    def create_mandatory_files(self):
        for path in self.MANDATORY_FILES:
            self.builtin_gen.copy_builtin_files(path_source=path, path_target=path)

    def run(self):
        self.create_mandatory_dirs()
        self.create_mandatory_files()
        print("Base directories and files created successfully.")
