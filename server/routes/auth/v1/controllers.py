from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models.sql.accounts import Account
from server.core.schemas.utilities import MessageResponse
from server.repositories.auth.create import create_user
from server.repositories.auth.read import get_account_by_email, get_account_by_username
from server.schemas.requests.auth import SignupRequest
from server.utils.exceptions import ConflictError


async def check_auth_service() -> MessageResponse:
    return MessageResponse(msg="Auth service is up and running!")


async def register_user(session: AsyncSession, payload: SignupRequest) -> Account:
    is_username_available = await get_account_by_username(session, payload.username)
    if is_username_available:
        raise ConflictError("Provided username already used by another account.")

    is_email_available = await get_account_by_email(session, payload.email)
    if is_email_available:
        raise ConflictError("Provided email address already used by another account.")

    try:
        account = await create_user(session, payload)
        return account
    except ConflictError as e:
        raise e
