from datetime import datetime

import inflection
from pydantic import BaseModel
from sqlalchemy import DateTime, Integer, event
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.schema import FetchedValue
from sqlalchemy.sql import functions
from sqlalchemy.types import TypeDecorator


class Base(DeclarativeBase):
    """Define a series of common elements that may be applied to mapped classes
    using this class as a base class."""

    @declared_attr
    def __tablename__(cls) -> str:
        return inflection.pluralize(inflection.underscore(cls.__name__))

    __mapper_args__ = {"eager_defaults": True}

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=functions.now(),
    )
    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_onupdate=FetchedValue(for_update=True),
        onupdate=functions.now(),
    )
    delete_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=None,
    )
    revision_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        event.listen(cls, "before_update", cls._increment_revision_id)

    @staticmethod
    def _increment_revision_id(mapper, connection, target):
        target.revision_id += 1


class PydanticJSONType(TypeDecorator):
    impl = JSON

    def __init__(self, model: BaseModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.model_dump()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self.model(**value)
        return value
