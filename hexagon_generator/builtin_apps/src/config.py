from pydantic_settings import BaseSettings

from src.common.loggin_config import setup_logger

logger = setup_logger()


class Settings(BaseSettings):
    database_url: str
    env_type: str
    frontend_url: str
    secret_key: str

    class Config:
        env_file = "../env_vars/backend.env"
        env_file_encoding = "utf-8"


settings = Settings()
