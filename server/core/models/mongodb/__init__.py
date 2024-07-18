from datetime import datetime, timezone

import inflection
from beanie import Document
from pydantic import Field


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
