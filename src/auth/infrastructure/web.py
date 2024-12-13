from fastapi import APIRouter, Depends
from src.auth.application.use_cases.auth import AuthUseCase
from src.auth.infrastructure.database import UserRepository
from src.auth.application.service import AuthService
from src.common.database_connection import get_db

router = APIRouter()
SECRET_KEY = "somethingspecial"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


@router.post("/login")
def login(identification: str, password: str, db=Depends(get_db)):
    auth_service = AuthService(
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        access_token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    user_repo = UserRepository()
    auth_use_case = AuthUseCase(auth_repo=user_repo, auth_service=auth_service)
    user = auth_use_case.authenticate_user(db, identification, password)
    if not user:
        return {"error": "Invalid credentials"}
    token = auth_service.create_access_token(data={"sub": user.identification})
    return {"access_token": token, "token_type": "bearer"}
