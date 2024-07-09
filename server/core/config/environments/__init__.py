from pydantic import EmailStr, HttpUrl, field_validator

from server.core.config.sources import ConfigSource


class AppConfig(ConfigSource):
    APP_NAME: str
    VERSION: str
    API_PREFIX: str
    TERMS_OF_SERVICE: HttpUrl

    # Maintainer Contact
    MAINTAINER_NAME: str
    MAINTAINER_ONLINE_PROFILE: HttpUrl
    MAINTAINER_EMAIL: EmailStr

    @field_validator("API_PREFIX")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        return f"/{value.strip('/')}"
