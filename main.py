from fastapi import FastAPI, HTTPException
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
from pydantic import BaseModel
from typing import Optional


class GeneratorRequest(BaseModel):
    type: str  # "crud" o "builtin"
    pascal_case: Optional[str] = None
    snake_case: Optional[str] = None
    builtin_app: Optional[str] = None


app = FastAPI()
HTTP_ACTIONS = ["create", "list", "retrieve", "update", "delete"]


@app.post("/generate/")
def generate_code(req: GeneratorRequest):
    # Inicializar generadores base
    builtin_generator = BuiltInGenerator()
    BaseDirsGenerator(builtin_gen=builtin_generator).run()

    if req.type == "crud":
        if not req.pascal_case or not req.snake_case:
            raise HTTPException(
                status_code=400,
                detail="For 'crud', 'pascal_case' and 'snake_case' are required.",
            )

        code_generator = CodeGenerator(
            pascal_case=req.pascal_case,
            snake_case=req.snake_case,
            HTTP_ACTIONS=HTTP_ACTIONS,
        )

        ModelGenerator(
            pascal_case=req.pascal_case,
            snake_case=req.snake_case,
            dirs=crud_dirs,
            routes=crud_routes,
            actions=HTTP_ACTIONS,
            use_cases_init=APPLICATION_WEB_CASE_TEMPLATE_INIT,
            use_cases=APPLICATION_WEB_CASE_TEMPLATE,
            code_generator=code_generator,
        ).run()

        return {"status": "success", "message": "CRUD files generated."}

    elif req.type == "builtin":
        if not req.builtin_app or req.builtin_app not in ["user"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid or missing builtin_app. Must be one of: ['user']",
            )

        path = f"src/{req.builtin_app}"
        builtin_generator.copy_builtin_apps(path_source=path, path_target=path)

        return {
            "status": "success",
            "message": f"Builtin app '{req.builtin_app}' copied.",
        }

    else:
        raise HTTPException(status_code=400, detail=f"Unknown type: {req.type}")
