from pydantic import field_validator

from server.core.models.redis import BaseCache, TimestampMixin
from server.schemas.responses.accounts import AccountResponse


class JWTStore(BaseCache, TimestampMixin, AccountResponse):
    is_active: int
    is_verified: int
    refresh_token: str

    @field_validator("is_active", "is_verified", mode="before")
    @classmethod
    def convert_boolean(cls, v: bool) -> int:
        return 1 if v else 0
