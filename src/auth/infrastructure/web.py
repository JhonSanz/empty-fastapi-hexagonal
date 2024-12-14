from fastapi import APIRouter, Depends
from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.infrastructure.database import UserRepository
from src.auth.application.service import AuthService
from src.common.database_connection import get_db
from src.auth.application.handlers import auth_handler

router = APIRouter()
SECRET_KEY = "somethingspecial"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


@router.post("/login")
async def login(identification: str, password: str, database=Depends(get_db)):
    auth_service = AuthService(
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        access_token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    user_repo = UserRepository()
    auth_use_case = AuthUseCase(
        database=database, auth_repo=user_repo, auth_service=auth_service
    )
    token = await auth_handler(
        identification=identification, password=password, auth_use_case=auth_use_case
    )
    return {"access_token": token, "token_type": "bearer"}


# def get_auth_use_case(db: Session = Depends(get_db)) -> AuthUseCase:
#     auth_repo = UserRepository()  # Instancia tu repositorio
#     auth_service = AuthService()  # Instancia tu servicio
#     return AuthUseCase(database=db, auth_repo=auth_repo, auth_service=auth_service)


# def get_user_with_permission(required_permission: str):
#     def get_current_active_user(
#         authorization: str = Header(
#             ...
#         ),  # Asumiendo que el token está en el header "Authorization"
#         db: Session = Depends(get_db),
#         auth_use_case: AuthUseCase = Depends(get_auth_use_case),
#     ):
#         # Extraer el token del encabezado
#         token = authorization.replace("Bearer ", "")
#         user = auth_use_case.get_current_user(token=token)

#         # Aquí deberías verificar si el usuario tiene el permiso adecuado
#         permission_checker(db=db, permission=required_permission, user=user)
#         return user

#     return get_current_active_user
