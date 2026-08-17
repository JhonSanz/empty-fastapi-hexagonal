from fastapi import APIRouter, Depends

from src.cognito_auth.application.schemas import CognitoUser
from src.cognito_auth.dependencies.get_user_with_permissions import get_current_user
from src.common.std_response import StandardResponse, std_response


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.get(
    "/me",
    response_model=StandardResponse[CognitoUser],
)
async def me(user: CognitoUser = Depends(get_current_user)):
    """
    Bootstrap endpoint for the frontend: verifies the Cognito ID token and
    returns the resolved local profile + permissions. There's no /token
    endpoint here — login itself happens against Cognito directly.
    """
    return std_response(data=user)
