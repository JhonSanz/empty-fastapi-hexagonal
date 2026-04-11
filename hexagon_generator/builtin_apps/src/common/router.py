from fastapi import APIRouter

from src.user.infrastructure.web import router as user_router
from src.role.infrastructure.web import router as role_router
from src.auth.infrastructure.web import router as auth_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(role_router)
api_router.include_router(auth_router)
