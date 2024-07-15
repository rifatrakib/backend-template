from pydantic import Field, field_validator

from server.core.schemas import BaseRequestSchema
from server.dependencies.fields import email_field, name_field, password_field, username_field
from server.utils.exceptions import RequestValidationError
from server.utils.helpers import validate_password_pattern


class SignupRequest(BaseRequestSchema):
    username: str = username_field(Field)
    email: str = email_field(Field)
    password: str = password_field(Field)
    first_name: str = name_field(Field, "first")
    middle_name: str | None = name_field(Field, "middle", default=None)
    last_name: str = name_field(Field, "last")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        try:
            return validate_password_pattern(v)
        except ValueError as e:
            raise RequestValidationError(e.args[0])

    @staticmethod
    def form_example(metadata: dict[str, str]) -> dict[str, str]:
        examples = {
            "username": {"example": "john_doe"},
            "email": {"example": "john.doe@example.com"},
            "password": {"example": "Pass@1234"},
            "first_name": {"example": "John"},
            "middle_name": {"example": "Doe"},
            "last_name": {"example": "Smith"},
        }
        for key, value in examples.items():
            metadata[key]["example"] = value["example"]
        return metadata
