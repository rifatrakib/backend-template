from aredis_om.model import NotFoundError

from server.models.redis.mail import AccountActivationCache
from server.utils.exceptions import NoDataFoundError


async def read_activation_cache(key: str) -> AccountActivationCache:
    try:
        return await AccountActivationCache.get(key.upper())
    except NotFoundError:
        raise NoDataFoundError("Link is forged or expired.")
