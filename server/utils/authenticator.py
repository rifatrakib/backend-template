from datetime import datetime, timedelta, timezone
from typing import Any

from aredis_om.model.model import NotFoundError
from jose import JWTError, jwt
from pydantic import ValidationError

from server.core.config import settings
from server.core.models.sql.accounts import Account
from server.models.redis.jwt import JWTStore
from server.schemas.responses.accounts import AccountResponse, JWTPayload, JWTResponse
from server.utils.exceptions import NoDataFoundError, NotAuthenticatedError, NotPermittedError
from server.utils.managers import password_manager


def authenticate_user(account: Account | None, username: str, password: str) -> bool:
    if not account:
        raise NoDataFoundError(f"No account registered for {username}.")

    if not account.is_active:
        raise NotPermittedError("Account not active. Please activate your account with email.")

    if not password_manager.verify_password(password, account.hash_salt, account.hashed_password):
        raise NotAuthenticatedError("Wrong credentials")

    return True


def create_access_token(data: AccountResponse) -> str:
    to_encode = JWTPayload(
        **data.model_dump(),
        sub=settings.ACCESS_TOKEN_SUBJECT,
        exp=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY),
    )

    return jwt.encode(
        to_encode.model_dump(),
        key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ACCESS_TOKEN_ALGORITHM,
    )


def create_refresh_token(data: AccountResponse) -> str:
    to_encode = JWTPayload(
        **data.model_dump(),
        sub=settings.REFRESH_TOKEN_SUBJECT,
        exp=datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRY),
    )

    return jwt.encode(
        to_encode.model_dump(),
        key=settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm=settings.REFRESH_TOKEN_ALGORITHM,
    )


async def get_jwt(data: Any) -> tuple[JWTResponse, AccountResponse]:
    account_data = AccountResponse.model_validate(data)
    access_token = create_access_token(account_data)
    refresh_token = create_refresh_token(account_data)
    return JWTResponse(access_token=access_token, refresh_token=refresh_token), account_data


async def generate_jwt(account: Account) -> JWTResponse:
    jwt, account_data = await get_jwt(account)
    await JWTStore(refresh_token=jwt.refresh_token, **account_data.model_dump()).save()
    return jwt


def decode_access_token(token: str) -> AccountResponse:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[settings.ACCESS_TOKEN_ALGORITHM],
        )
        return AccountResponse.model_validate(payload)
    except JWTError:
        raise ValueError("unable to decode JWT")
    except ValidationError:
        raise ValueError("invalid payload in JWT")


async def generate_jwt_from_refresh_token(token: str) -> JWTResponse:
    try:
        payload = await JWTStore.get(token)
        await JWTStore.delete(token)
        jwt, account_data = await get_jwt(payload)
        await JWTStore(**account_data.model_dump()).save()
        return jwt
    except NotFoundError:
        raise NoDataFoundError("Invalid refresh token")
