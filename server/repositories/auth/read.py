from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models.sql.accounts import Account


async def get_account_by_email(session: AsyncSession, email: str) -> Account:
    result = await session.execute(select(Account).filter(Account.email == email))
    return result.scalars().first()


async def get_account_by_username(session: AsyncSession, username: str) -> Account:
    result = await session.execute(select(Account).filter(Account.username == username))
    return result.scalars().first()
