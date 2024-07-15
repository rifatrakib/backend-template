import re


def validate_password_pattern(password: str) -> str:
    """Validate password contains at least one uppercase letter, one lowercase
    letter, one digit and one special character.

    Return password if valid.
    """

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$"
    if not re.match(pattern, password):
        raise ValueError(
            "Password must be between 8 and 64 characters long and contain at least one uppercase letter, one lowercase letter, one"
            " digit and one special character."
        )
    return password
