import jwt
from jwt import PyJWKClient

from src.config import settings
from src.cognito_auth.domain.exceptions import (
    CognitoNotConfiguredException,
    InvalidTokenException,
)


class CognitoTokenVerifier:
    """
    Verifies a Cognito **ID token** against the User Pool's public JWKS.

    We verify the ID token (not the Access token) because it carries the
    `email` claim we need to provision/match a local user record. If you
    set up a Cognito Resource Server with custom scopes and want to
    authorize purely on `scope` instead of the local Role/Permission
    tables, verify the Access token here instead — but then you lose
    `email` from the token and have to source it another way (e.g. only
    from a Post Confirmation Lambda sync, never from the live request).
    """

    def __init__(self):
        if not (
            settings.cognito_user_pool_id
            and settings.cognito_region
            and settings.cognito_app_client_id
        ):
            raise CognitoNotConfiguredException(
                "COGNITO_USER_POOL_ID, COGNITO_REGION and COGNITO_APP_CLIENT_ID "
                "must be set to use cognito_auth"
            )

        self.issuer = (
            f"https://cognito-idp.{settings.cognito_region}.amazonaws.com/"
            f"{settings.cognito_user_pool_id}"
        )
        self._jwk_client = PyJWKClient(f"{self.issuer}/.well-known/jwks.json")

    def verify(self, token: str) -> dict:
        try:
            signing_key = self._jwk_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.cognito_app_client_id,
                issuer=self.issuer,
            )
        except jwt.PyJWTError as e:
            raise InvalidTokenException(str(e))

        if payload.get("token_use") != "id":
            raise InvalidTokenException("Expected a Cognito ID token")

        return payload


_verifier: CognitoTokenVerifier | None = None


def get_verifier() -> CognitoTokenVerifier:
    """Lazily build a singleton so PyJWKClient's key cache is reused across requests."""
    global _verifier
    if _verifier is None:
        _verifier = CognitoTokenVerifier()
    return _verifier
