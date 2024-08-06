from datetime import date

from pydantic import ConfigDict, EmailStr, Field, field_validator

from server.core.enums import Genders
from server.core.schemas import BaseRequestSchema
from server.dependencies.fields import birthdate_field, email_field, gender_field, name_field, password_field, username_field
from server.utils.exceptions import RequestValidationError
from server.utils.helpers import validate_password_pattern


class EmailBodyInput(BaseRequestSchema):
    email: EmailStr = email_field(Field)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "test@example.io",
                },
            ],
        },
    )


class SignupRequest(EmailBodyInput):
    username: str = username_field(Field, pattern=r"^[a-zA-Z0-9_]{4,64}$")
    password: str = password_field(Field)
    first_name: str = name_field(Field, "first", pattern=r"^[a-zA-Z]{2,64}$")
    middle_name: str | None = name_field(Field, "middle", default=None, pattern=r"^[a-zA-Z]{2,256}$")
    last_name: str = name_field(Field, "last", pattern=r"^[a-zA-Z]{2,64}$")
    gender: Genders | None = gender_field(Field, default=None)
    birth_date: date | None = birthdate_field(Field, default=None)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "johndoe",
                    "email": "mail@example.com",
                    "password": "Pass@12345",  # pragma: allowlist secret
                    "first_name": "John",
                    "middle_name": "Smith",
                    "last_name": "Doe",
                    "gender": "m",
                    "birth_date": "2014-07-19",
                },
            ],
        },
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        try:
            return validate_password_pattern(v)
        except ValueError as e:
            raise RequestValidationError(e.args[0])

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        # validate that the date is not bigger than today's date
        if v > date.today():
            raise RequestValidationError("Birth date cannot be in the future.")
        return v


class LoginRequest(BaseRequestSchema):
    username: str = username_field(Field)
    password: str = password_field(Field)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "johndoe",
                    "password": "Pass@12345",  # pragma: allowlist secret
                },
            ],
        },
    )
