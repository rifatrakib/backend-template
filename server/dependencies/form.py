from datetime import date
from typing import Annotated

from fastapi import Form

from server.core.enums import Genders
from server.dependencies.fields import birthdate_field, email_field, gender_field, name_field, password_field, username_field
from server.schemas.requests.auth import SignupRequest


def signup_form(
    username: Annotated[str, username_field(Form, pattern=r"^[a-zA-Z0-9_]{4,64}$")],
    email: Annotated[str, email_field(Form)],
    password: Annotated[str, password_field(Form)],
    first_name: Annotated[str, name_field(Form, "first", pattern=r"^[a-zA-Z]{2,64}$")],
    last_name: Annotated[str, name_field(Form, "last", pattern=r"^[a-zA-Z]{2,64}$")],
    middle_name: Annotated[str | None, name_field(Form, "middle", pattern=r"^[a-zA-Z]{2,256}$")] = None,
    gender: Annotated[Genders | None, gender_field(Form)] = None,
    birth_date: Annotated[date | None, birthdate_field(Form)] = None,
) -> SignupRequest:
    return SignupRequest(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        gender=gender,
        birth_date=birth_date,
    )
