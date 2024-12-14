from fastapi import APIRouter

# TODO:
from src.auth.infrastructure.web import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
