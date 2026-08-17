from dataclasses import dataclass


@dataclass
class User:
    """Local shadow profile for a Cognito-authenticated identity."""

    id: int
    cognito_sub: str
    name: str
    email: str
    phone: str
    is_active: bool


@dataclass
class CreateUserData:
    cognito_sub: str
    name: str
    email: str
    phone: str = ""
    is_active: bool = True


@dataclass
class UpdateUserData:
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    is_active: bool | None = None
