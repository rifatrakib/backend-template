from datetime import datetime

import inflection
from sqlalchemy import DateTime, ForeignKey, Integer, event
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.sql import functions


class Base(DeclarativeBase):
    """Define a series of common elements that may be applied to mapped classes
    using this class as a base class."""

    @declared_attr
    def __tablename__(cls) -> str:
        return inflection.pluralize(inflection.underscore(cls.__name__))

    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
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

    @declared_attr
    def creator_id(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("accounts.id"), nullable=True)

    @declared_attr
    def last_updator_id(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("accounts.id"), nullable=True)

    @declared_attr
    def deletor_id(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("accounts.id"), nullable=True)

    @declared_attr
    def created_by(cls) -> Mapped["Account"]:  # noqa: F821
        return relationship("Account", foreign_keys=[cls.creator_id])

    @declared_attr
    def last_updated_by(cls) -> Mapped["Account"]:  # noqa: F821
        return relationship("Account", foreign_keys=[cls.last_updator_id])

    @declared_attr
    def deleted_by(cls) -> Mapped["Account"]:  # noqa: F821
        return relationship("Account", foreign_keys=[cls.deletor_id])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        event.listen(cls, "before_update", cls._increment_revision_id)

    @staticmethod
    def _increment_revision_id(mapper, connection, target):
        target.revision_id += 1
