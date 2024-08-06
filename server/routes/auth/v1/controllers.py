from fastapi import BackgroundTasks, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.config import settings
from server.core.schemas.utilities import MessageResponse
from server.events.auth.signup import account_activation_success_event, signup_success_event
from server.models.redis.jwt import JWTStore
from server.repositories.auth.cache import read_activation_cache
from server.repositories.auth.create import create_user
from server.repositories.auth.read import get_account_by_email, get_account_by_email_or_username, get_account_by_username
from server.repositories.auth.update import activate_account_status
from server.schemas.requests.auth import LoginRequest, SignupRequest
from server.schemas.responses.accounts import JWTResponse
from server.utils.authenticator import authenticate_user, generate_jwt, generate_jwt_from_refresh_token
from server.utils.exceptions import BadRequestError, ConflictError, NoDataFoundError
from server.utils.mail.tasks import process_account_activation, send_activation_successful_mail


async def check_auth_service() -> MessageResponse:
    return MessageResponse(msg="Auth service is up and running!")


async def protected_check():
    return MessageResponse(msg="Authentication is working on protected endpoint!")


async def register_user(
    request: Request,
    queue: BackgroundTasks,
    session: AsyncSession,
    payload: SignupRequest,
) -> MessageResponse:
    is_username_available = await get_account_by_username(session, payload.username)
    if is_username_available:
        raise ConflictError("Provided username already used by another account.")

    is_email_available = await get_account_by_email(session, payload.email)
    if is_email_available:
        raise ConflictError("Provided email address already used by another account.")

    try:
        account = await create_user(session, payload)
        queue.add_task(signup_success_event, account)
        return await process_account_activation(request, queue, account)
    except HTTPException as e:
        raise e


async def login_active_user(session: AsyncSession, payload: LoginRequest) -> JWTResponse:
    try:
        account = await get_account_by_email_or_username(session, payload.username)
        if not account:
            raise NoDataFoundError(f"No account registered for {payload.username}.")

        authenticate_user(account, payload.password)
        return await generate_jwt(account)
    except HTTPException as e:
        raise e


async def refresh(token: str) -> JWTResponse:
    try:
        return await generate_jwt_from_refresh_token(token)
    except HTTPException as e:
        raise e


async def logout(token: str):
    await JWTStore.delete(token)


async def check_activation_link(key: str):
    try:
        await read_activation_cache(key)
    except HTTPException as e:
        raise e


async def activate_account(
    request: Request,
    queue: BackgroundTasks,
    session: AsyncSession,
    key: str,
) -> MessageResponse:
    try:
        activation_cache = await read_activation_cache(key)
        account = await activate_account_status(session, activation_cache.id)
        queue.add_task(account_activation_success_event, account)

        if settings.SEND_MAIL:
            queue.add_task(send_activation_successful_mail, request, account)

        return MessageResponse(msg="Account activation successful.")
    except HTTPException as e:
        raise e


async def resend_account_activation_mail(
    request: Request,
    queue: BackgroundTasks,
    payload: SignupRequest,
    session: AsyncSession,
):
    try:
        account = await get_account_by_email(session, payload.email)
        if not account:
            raise NoDataFoundError("No account found with the provided email address.")
        if account.is_active:
            raise BadRequestError("Account is already active.")
        return await process_account_activation(request, queue, account)
    except HTTPException as e:
        raise e
