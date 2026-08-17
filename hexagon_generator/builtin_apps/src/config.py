from pydantic_settings import BaseSettings, SettingsConfigDict

from src.common.loggin_config import setup_logger

logger = setup_logger()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../env_vars/backend.env",
        env_file_encoding="utf-8",
    )

    database_url: str
    env_type: str
    frontend_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Only needed if using the `cognito_auth` builtin instead of `auth`.
    cognito_user_pool_id: str | None = None
    cognito_region: str | None = None
    cognito_app_client_id: str | None = None


settings = Settings()
