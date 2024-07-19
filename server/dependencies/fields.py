from typing import Callable

from pydantic.fields import FieldInfo


def username_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Username",
        description="The unique username of the user.",
        **kwargs,
    )


def email_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Email",
        description="The unique email address of the user.",
        **kwargs,
    )


def password_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Password",
        description="The password of the user containing at least one uppercase letter, one lowercase letter, and one digit.",
        **kwargs,
    )


def name_field(Function: Callable[..., FieldInfo], position: str, **kwargs) -> FieldInfo:
    return Function(
        title=f"{position.capitalize()} Name",
        description=f"The {position} name of the user.",
        **kwargs,
    )


def gender_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Gender",
        description="Gender of the user (m: male, f: female).",
        **kwargs,
    )


def birthdate_field(Function: Callable[..., FieldInfo], **kwargs) -> FieldInfo:
    return Function(
        title="Birthdate",
        description="The birthdate of the user in the format of YYYY-MM-DD.",
        **kwargs,
    )
