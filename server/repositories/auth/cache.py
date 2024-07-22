from aredis_om.model import NotFoundError

from server.models.redis.accounts import SignupCache
from server.schemas.requests.auth import SignupRequest
from server.utils.exceptions import NoDataFoundError


async def check_activation_link_key(key: str) -> None:
    try:
        await SignupCache.get(key.upper())
    except NotFoundError:
        raise NoDataFoundError("Link is forged or expired.")


async def read_cached_account_data(key: str) -> SignupRequest:
    try:
        return SignupRequest.model_validate(await SignupCache.get(key.upper()))
    except NotFoundError:
        raise NoDataFoundError("Link is forged or expired.")
