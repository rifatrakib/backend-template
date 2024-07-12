from server.core.schemas import BaseConfig


class Config(BaseConfig):
    MONGODB_USER: str | None = None
    MONGODB_PASSWORD: str | None = None
    MONGODB_HOST: str
    MONGODB_PORT: int

    # Timeseries configuration
    BUCKET_MAX_SPAN_SECONDS: int
    BUCKET_ROUNDING_SECONDS: int
    EXPIRE_AFTER_SECONDS: int

    @property
    def MONGO_URI(self):
        user = self.MONGODB_USER
        password = self.MONGODB_PASSWORD
        host = self.MONGODB_HOST
        port = self.MONGODB_PORT

        if user is None or password is None:
            return f"mongodb://{host}:{port}"
        return f"mongodb://{user}:{password}@{host}:{port}"
