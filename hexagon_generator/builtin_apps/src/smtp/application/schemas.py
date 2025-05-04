from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.common.base_schemas import BaseModelWithNoneCheck


class SMTPInDBBase(BaseModel):
    id: int
    server: str
    port: str
    user: str
    password: str
    receivers: Optional[list[str]] = None


class CreateSMTPRequest(BaseModel):
    server: str
    port: str
    user: str
    password: str
    receivers: Optional[list[str]] = None


class UpdateSMTPRequest(BaseModelWithNoneCheck):
    server: Optional[str] = None
    port: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    receivers: Optional[list[str]] = None


class SMTPBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    host: str
    port: str
    user: str
    password: str
    receivers: Optional[list[str]] = None
    debug: bool


class FilterParams(BaseModel):
    skip: int = 0
    limit: int = 10
