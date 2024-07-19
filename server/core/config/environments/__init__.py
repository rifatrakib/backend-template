from pydantic import EmailStr, HttpUrl, field_validator

from server.core.config.db_config import DatabaseConfig
from server.core.config.sources import ConfigSource


class AppConfig(ConfigSource, DatabaseConfig):
    APP_NAME: str
    VERSION: str
    API_PREFIX: str
    TERMS_OF_SERVICE: HttpUrl
    TEST_RUN: bool

    # Maintainer Contact
    MAINTAINER_NAME: str
    MAINTAINER_ONLINE_PROFILE: HttpUrl
    MAINTAINER_EMAIL: EmailStr

    # Password Hashing Configurations
    PASSWORD_HASH_ALGORITHM: str
    HASH_ROUNDS: int

    # Mail Configurations
    MAIL_USERNAME: EmailStr | str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool

    @field_validator("API_PREFIX")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        return f"/{value.strip('/')}"

    @property
    def hash_round_settings(self) -> dict:
        if self.PASSWORD_HASH_ALGORITHM == "bcrypt":  # pragma: allowlist secret
            return {"bcrypt__default_rounds": self.HASH_ROUNDS}
        if self.PASSWORD_HASH_ALGORITHM == "argon2":  # pragma: allowlist secret
            return {"argon2__time_cost": self.HASH_ROUNDS}
