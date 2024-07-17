from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models.sql.accounts import Account
from server.schemas.requests.auth import SignupRequest
from server.utils.exceptions import ConflictError
from server.utils.managers import password_manager


async def create_user(session: AsyncSession, payload: SignupRequest) -> Account:
    account = Account(
        username=payload.username,
        email=payload.email,
        first_name=payload.first_name,
        middle_name=payload.middle_name,
        last_name=payload.last_name,
    )

    hash_salt = password_manager.generate_hash_salt()
    account.set_hash_salt(hash_salt)
    account.set_hashed_password(
        password_manager.generate_hashed_password(hash_salt, payload.password),
    )

    try:
        session.add(account)
        await session.commit()
        await session.refresh(account)
        return account
    except IntegrityError as e:
        await session.rollback()
        raise ConflictError(e.args[0])
