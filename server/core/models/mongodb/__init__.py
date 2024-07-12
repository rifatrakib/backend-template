from datetime import datetime, timezone

import inflection
from beanie import Document, Granularity, TimeSeriesConfig
from pydantic import Field

from server.core.config import settings
from server.core.models.mongodb.schemas import MetadataField


class BaseDocument(Document):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        use_cache = True
        use_revision = True
        use_state_management = True
        validation_on_save = True

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.Settings.name = inflection.pluralize(inflection.underscore(cls.__name__))


class BaseTimeseriesDocument(BaseDocument):
    metadata: MetadataField = Field(default_factory=dict)

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="created_at",
            meta_field="metadata",
            granularity=Granularity.seconds,
            bucket_max_span_seconds=settings.BUCKET_MAX_SPAN_SECONDS,
            bucket_rounding_seconds=settings.BUCKET_ROUNDING_SECONDS,
            expire_after_seconds=settings.EXPIRE_AFTER_SECONDS,
        )
