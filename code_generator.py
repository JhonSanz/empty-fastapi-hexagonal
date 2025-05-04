import argparse
from hexagon_generator.core.base_check_gen import BaseDirsGenerator
from hexagon_generator.core.builtin_gen import BuiltInGenerator
from hexagon_generator.core.code_gen import CodeGenerator
from hexagon_generator.core.model_gen import ModelGenerator
from hexagon_generator.templates.crud.application_web_cases import (
    APPLICATION_WEB_CASE_TEMPLATE,
    APPLICATION_WEB_CASE_TEMPLATE_INIT,
)
from hexagon_generator.templates.crud.routes import (
    routes as crud_routes,
    dirs as crud_dirs,
)

HTTP_ACTIONS = ["create", "list", "retrieve", "update", "delete"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generador de archivos hexagonales para CRUD."
    )
    parser.add_argument("type", type=str, help="Behaviuor: [crud, builtin].")
    parser.add_argument(
        "pascal_case", type=str, nargs="?", help="Nombre del modelo (PascalCase)."
    )
    parser.add_argument(
        "snake_case", type=str, nargs="?", help="Nombre del modelo (snake_case)."
    )
    parser.add_argument("builtin_app", type=str, nargs="?", help="Enabled apps: [user]")

    args = parser.parse_args()
    builtin_generator = BuiltInGenerator()
    BaseDirsGenerator(builtin_gen=builtin_generator).run()

    if args.type == "crud":
        if not args.pascal_case or not args.snake_case:
            parser.error(
                "For 'crud' option, arguments 'pascal_case' and 'snake_case' are mandatory."
            )
        code_generator = CodeGenerator(
            pascal_case=args.pascal_case,
            snake_case=args.snake_case,
            HTTP_ACTIONS=HTTP_ACTIONS,
        )
        ModelGenerator(
            pascal_case=args.pascal_case,
            snake_case=args.snake_case,
            dirs=crud_dirs,
            routes=crud_routes,
            actions=HTTP_ACTIONS,
            use_cases_init=APPLICATION_WEB_CASE_TEMPLATE_INIT,
            use_cases=APPLICATION_WEB_CASE_TEMPLATE,
            code_generator=code_generator,
        ).run()
    elif args.type == "builtin":
        if not args.builtin_app or not args.builtin_app in ["user"]:
            parser.error(
                f"For 'builtin' option, argument {args.builtin_app} is mandatory or not in the list."
            )

        path = f"src/{args.type}"
        builtin_generator.copy_builtin_apps(path_source=path, path_target=path)
    else:
        parser.error(f"Unknown type: {args.type}")
