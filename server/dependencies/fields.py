from typing import Callable

from pydantic.fields import FieldInfo


def username_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Username",
        description="The unique username of the user.",
        openapi_examples={
            "valid": {"summary": "Valid username", "value": "john_doe"},
            "invalid": {"summary": "Invalid username", "value": "john doe"},
        },
        **kwargs,
    )


def email_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Email",
        description="The unique email address of the user.",
        openapi_examples={
            "valid": {"summary": "Valid email", "value": "mail@example.com"},
            "invalid": {"summary": "Invalid email", "value": "mail@example"},
        },
        **kwargs,
    )


def password_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Password",
        description="The password of the user containing at least one uppercase letter, one lowercase letter, and one digit.",
        openapi_examples={
            "valid": {"summary": "Valid password", "value": "Password123"},
            "invalid": {"summary": "Invalid password", "value": "password"},
        },
        **kwargs,
    )


def name_field(Function: Callable[..., FieldInfo], position: str, **kwargs) -> FieldInfo:
    return Function(
        title=f"{position.capitalize()} Name",
        description=f"The {position} name of the user.",
        openapi_examples={
            "valid": {"summary": f"Valid {position} name", "value": "John Doe"},
            "invalid": {"summary": f"Invalid {position} name", "value": "John"},
        },
        **kwargs,
    )


def gender_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Gender",
        description="Gender of the user (m: male, f: female).",
        openapi_examples={
            "valid": {"summary": "Valid gender", "value": "m"},
            "invalid": {"summary": "Invalid gender", "value": "o"},
        },
        **kwargs,
    )


def birthdate_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Birthdate",
        description="The birthdate of the user in the format of YYYY-MM-DD.",
        openapi_examples={
            "valid": {"summary": "Valid birthdate", "value": "2000-01-01"},
            "invalid": {"summary": "Invalid birthdate", "value": "2000-01"},
        },
        **kwargs,
    )
