from datetime import date

from pydantic import Field, field_validator

from server.core.enums import Genders
from server.core.schemas import BaseRequestSchema
from server.dependencies.fields import birthdate_field, email_field, gender_field, name_field, password_field, username_field
from server.utils.exceptions import RequestValidationError
from server.utils.helpers import validate_password_pattern


class SignupRequest(BaseRequestSchema):
    username: str = username_field(Field)
    email: str = email_field(Field)
    password: str = password_field(Field)
    first_name: str = name_field(Field, "first")
    middle_name: str | None = name_field(Field, "middle", default=None)
    last_name: str = name_field(Field, "last")
    gender: Genders | None = gender_field(Field, default=None)
    birth_date: date | None = birthdate_field(Field, default=None)

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

    @staticmethod
    def form_example(metadata: dict[str, str]) -> dict[str, str]:
        examples = {
            "username": {"example": "john_doe"},
            "email": {"example": "john.doe@example.com"},
            "password": {"example": "Pass@1234"},
            "first_name": {"example": "John"},
            "middle_name": {"example": "Doe"},
            "last_name": {"example": "Smith"},
            "gender": {"example": "m"},
            "birth_date": {"example": "1990-01-01"},
        }

        for key, value in examples.items():
            metadata[key]["example"] = value["example"]
        return metadata
