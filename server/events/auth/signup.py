from server.core.models.sql.accounts import Account
from server.repositories.logs.changes import account_insert_log


async def signup_success_event(account: Account):
    await account_insert_log(account)
