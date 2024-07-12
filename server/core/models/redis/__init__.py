from abc import ABC
from datetime import datetime, timezone

from aredis_om import Field, HashModel
from aredis_om.connections import get_redis_connection

from server.core.config import settings
from server.core.schemas import BaseSchema


class BaseCache(HashModel, BaseSchema, ABC):
    class Meta:
        database = get_redis_connection(url=settings.REDIS_URI, decode_responses=True)
        global_key_prefix = settings.REDIS_GLOBAL_KEY_PREFIX


class TimestampMixin(BaseSchema):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
