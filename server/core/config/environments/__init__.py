from pydantic import field_validator

from server.core.config.sources import ConfigSource


class AppConfig(ConfigSource):
    APP_NAME: str
    VERSION: str
    API_PREFIX: str

    @field_validator("API_PREFIX")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        return f"/{value.strip('/')}"
