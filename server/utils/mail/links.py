from fastapi import Request

from server.core.config import settings
from server.core.models.sql.accounts import Account
from server.models.redis.mail import AccountActivationCache
from server.utils.helpers import extract_request_domain


async def get_account_activation_link(request: Request, account: Account) -> str:
    origin_host = extract_request_domain(request)
    data = AccountActivationCache(id=account.id, origin_host=origin_host)
    await data.save()
    await data.expire(settings.ACCOUNT_ACTIVATION_TTL)
    return f"{origin_host}/email-confirmation?key={data.pk.lower()}"
