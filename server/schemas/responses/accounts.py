from datetime import date

from pydantic import EmailStr, Field

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
