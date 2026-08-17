from pydantic import BaseModel, ConfigDict, Field


class CreateSMTPRequest(BaseModel):
    server: str
    port: str
    user: str
    password: str
    receivers: list[str] | None = None

    model_config = ConfigDict(extra="forbid")


class UpdateSMTPRequest(BaseModel):
    server: str | None = None
    port: str | None = None
    user: str | None = None
    password: str | None = None
    receivers: list[str] | None = None

    model_config = ConfigDict(extra="forbid")


class SMTPResponse(BaseModel):
    """API-facing SMTP config. Deliberately excludes `password`."""

    id: int = Field(..., gt=0)
    server: str
    port: str
    user: str
    receivers: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)


class SMTPBase(BaseModel):
    """Internal representation used to hand credentials to an SMTP provider."""

    model_config = ConfigDict(from_attributes=True)

    host: str
    port: str
    user: str
    password: str
    receivers: list[str] | None = None
    debug: bool


class FilterParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)
