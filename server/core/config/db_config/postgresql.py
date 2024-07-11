from server.core.schemas import BaseConfig


class Config(BaseConfig):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    @property
    def RDS_URI(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_HOST
        port = self.POSTGRES_PORT
        database = self.POSTGRES_DB
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
