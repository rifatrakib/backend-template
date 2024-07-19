from server.core.models.redis import BaseCache, TimestampMixin


class AccountActivationCache(BaseCache, TimestampMixin):
    id: int
    origin_host: str
