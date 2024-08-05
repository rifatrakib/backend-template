from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models.sql.accounts import Account
from server.utils.exceptions import NoDataFoundError


async def activate_account_status(session: AsyncSession, account_id: int) -> Account:
    account = await session.get(Account, account_id)

    if not account:
        raise NoDataFoundError(message=f"The account with id {account_id} is not registered.")

    account.is_active = True
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account
