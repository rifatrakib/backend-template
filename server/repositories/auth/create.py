from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models.mongodb.accounts import AccountCache
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

    if payload.gender:
        account.set_gender(payload.gender)
    if payload.birth_date:
        account.set_birth_date(payload.birth_date)

    try:
        session.add(account)
        await session.commit()
        await session.refresh(account)
        return account
    except IntegrityError as e:
        await session.rollback()
        raise ConflictError(e.args[0])


async def create_account_cache(payload: Account) -> None:
    account = AccountCache(
        account_id=payload.id,
        username=payload.username,
        email=payload.email,
        first_name=payload.first_name,
        middle_name=payload.middle_name,
        last_name=payload.last_name,
        birth_date=payload.birth_date,
        gender=payload.gender,
        is_active=payload.is_active,
        is_verified=payload.is_verified,
        is_superuser=payload.is_superuser,
    )
    await account.save()
