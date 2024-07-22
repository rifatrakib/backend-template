from server.core.models.redis import BaseCache, TimestampMixin
from server.schemas.requests.auth import SignupRequest


class SignupCache(BaseCache, TimestampMixin, SignupRequest):
    pass
