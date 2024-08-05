from typing import Annotated

from fastapi import Query


def temporary_key(key: Annotated[str, Query(..., description="Temporary link key with an expiry")]) -> str:
    return key


def refresh_token(token: Annotated[str, Query(..., description="Refresh token to renew access token")]) -> str:
    return token
