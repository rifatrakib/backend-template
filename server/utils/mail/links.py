from fastapi import Request

from server.core.config import settings
from server.models.redis.accounts import SignupCache
from server.schemas.requests.auth import SignupRequest
from server.utils.helpers import extract_request_domain


async def get_account_activation_link(request: Request, payload: SignupRequest) -> str:
    origin_host = extract_request_domain(request)
    data = SignupCache.model_validate(payload)
    await data.save()
    await data.expire(settings.ACCOUNT_ACTIVATION_TTL)
    return f"{origin_host}/email-confirmation?key={data.pk.lower()}"
