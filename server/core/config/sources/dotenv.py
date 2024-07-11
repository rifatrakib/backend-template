from server.core.schemas import BaseConfig


class ConfigSource(BaseConfig):
    SOURCE: str = ".env"
