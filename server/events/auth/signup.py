from server.core.config import settings
from server.core.models.sql.accounts import Account
from server.models.mongodb.events import ChangeLog
from server.schemas.responses.accounts import AccountResponse


async def signup_success_event(created_account: Account):
    log = ChangeLog(
        account_id=created_account.id,
        resource_name=f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
        object_name=Account.__tablename__,
        object_id=created_account.id,
        action="insert",
        new_value=AccountResponse.model_validate(created_account),
    )
    await log.insert()
