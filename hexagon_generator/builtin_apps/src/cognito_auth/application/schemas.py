from pydantic import BaseModel, Field


class CognitoUser(BaseModel):
    id: int
    cognito_sub: str
    email: str
    permissions: list[str] = Field(default_factory=list)
