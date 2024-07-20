from datetime import datetime, timedelta, timezone

from jose import jwt

from server.core.config import settings
from server.core.models.sql.accounts import Account
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


async def generate_jwt(account: Account) -> JWTResponse:
    account_data = AccountResponse.model_validate(account)
    access_token = create_access_token(account_data)
    refresh_token = create_refresh_token(account_data)
    # TODO: store the refresh token with account data in redis here
    return JWTResponse(access_token=access_token, refresh_token=refresh_token)
