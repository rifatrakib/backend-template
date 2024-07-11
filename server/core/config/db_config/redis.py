from server.core.schemas import BaseConfig


class Config(BaseConfig):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB_INDEX: int
    DEFAULT_TTL: int

    @property
    def REDIS_URI(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_INDEX}"
