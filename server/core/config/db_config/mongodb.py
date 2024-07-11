from server.core.schemas import BaseConfig


class Config(BaseConfig):
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_PORT: int

    @property
    def MONGO_URI(self):
        return f"mongodb://{self.MONGODB_USER}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}"
