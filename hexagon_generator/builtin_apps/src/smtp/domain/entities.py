from dataclasses import dataclass, field


@dataclass
class SMTPConfig:
    id: int
    server: str
    port: str
    user: str
    password: str
    receivers: list[str] = field(default_factory=list)


@dataclass
class CreateSMTPConfigData:
    server: str
    port: str
    user: str
    password: str
    receivers: list[str] = field(default_factory=list)


@dataclass
class UpdateSMTPConfigData:
    server: str | None = None
    port: str | None = None
    user: str | None = None
    password: str | None = None
    receivers: list[str] | None = None
