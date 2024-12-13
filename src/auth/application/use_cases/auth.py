from typing import Optional
from sqlalchemy.orm import Session
from src.auth.application.schemas import User
from src.auth.domain.repository import AuthRepository
from src.auth.application.service import AuthService
from fastapi import HTTPException, status
import jwt


class AuthUseCase:
    def __init__(self, auth_repo: AuthRepository, auth_service: AuthService):
        self.auth_repo = auth_repo
        self.auth_service = auth_service

    def authenticate_user(
        self, db: Session, identification: str, password: str
    ) -> Optional[User]:
        user = self.auth_repo.get_user_by_identification(db, identification)
        if not user or not self.auth_service.verify_password(password, user.password):
            return None
        return user

    def get_current_user(self, db: Session, token: str) -> User:
        try:
            payload = self.auth_service.decode_access_token(token)
            identification = payload.get("sub")
            if not identification:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user = self.user_repo.get_by_identification(db, identification)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )
            return user
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
