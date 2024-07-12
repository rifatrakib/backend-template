from server.core.schemas import BaseConfig


class Config(BaseConfig):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None
    DEFAULT_TTL: int
    REDIS_GLOBAL_KEY_PREFIX: str

    @property
    def REDIS_URI(self) -> str:
        if not self.REDIS_PASSWORD:
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"
