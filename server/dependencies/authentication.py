from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from server.schemas.responses.accounts import AccountResponse
from server.utils.authenticator import decode_access_token
from server.utils.exceptions import NotAuthenticatedError


def authenticate_active_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/openapi-login"))],
) -> AccountResponse:
    try:
        return decode_access_token(token)
    except ValueError:
        raise NotAuthenticatedError("Session expired. Please refresh your token.")
