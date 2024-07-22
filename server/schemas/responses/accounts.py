from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field, field_serializer

from server.core.config import settings
from server.core.enums import Genders
from server.core.schemas import BaseResponseSchema


class AccountResponse(BaseResponseSchema):
    id: int = Field(..., description="Unique identifier of the account.")
    username: str = Field(..., description="Username of the account.")
    email: EmailStr = Field(..., description="Email address of the account.")
    first_name: str = Field(..., description="First name of the account.")
    middle_name: str | None = Field(default=None, description="Middle name of the account.")
    last_name: str = Field(..., description="Last name of the account.")
    gender: Genders | None = Field(default=None, description="Gender of the account.")
    birth_date: date | None = Field(default=None, description="Birth date of the account.")
    is_active: bool = Field(..., description="Whether the account is active.")
    is_verified: bool = Field(..., description="Whether the account is verified.")

    @field_serializer("birth_date", when_used="always")
    def serialize_birthdate(self, v: date) -> str:
        return str(v)


class JWTPayload(AccountResponse):
    exp: datetime
    sub: str


class JWTResponse(BaseModel):
    access_token: str = Field(..., description="Access token generated for successful login with short expiry")
    refresh_token: str = Field(..., description="Refresh token generated for successful login with long expiry")
    token_type: str = Field(settings.TOKEN_TYPE, description="Token type for identification of token decryption method")
