from server.core.config import settings
from server.core.models.sql.accounts import Account
from server.models.mongodb.events import ChangeLog
from server.schemas.responses.accounts import AccountResponse


async def account_insert_log(account: Account):
    log = ChangeLog(
        account_id=account.id,
        resource_name=f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
        object_name=Account.__tablename__,
        object_id=account.id,
        action="insert",
        new_value=AccountResponse.model_validate(account),
    )
    await log.save()


async def account_update_log(account: Account):
    last_log = await ChangeLog.find(ChangeLog.account_id == account.id).sort(ChangeLog.created_at, -1).first_or_none()
    if last_log:
        last_log.old_value = last_log.new_value
        last_log.new_value = AccountResponse.model_validate(account)
        await last_log.save()
