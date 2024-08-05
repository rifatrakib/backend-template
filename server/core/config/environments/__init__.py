from pydantic import EmailStr, HttpUrl, field_validator

from server.core.config.sources import ConfigSource


class AppConfig(ConfigSource):
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
    SEND_MAIL: bool = True
    MAIL_USERNAME: EmailStr | str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool

    # JWT Configurations
    TOKEN_TYPE: str
    # Acccess Token
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_ALGORITHM: str
    ACCESS_TOKEN_SUBJECT: str
    ACCESS_TOKEN_EXPIRY: int
    # Refresh Token
    REFRESH_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_ALGORITHM: str
    REFRESH_TOKEN_SUBJECT: str
    REFRESH_TOKEN_EXPIRY: int

    # Temporary Link TTLs
    ACCOUNT_ACTIVATION_TTL: int = 60

    # PostgreSQL Configurations
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # MongoDB Configurations
    MONGODB_USER: str | None = None
    MONGODB_PASSWORD: str | None = None
    MONGODB_HOST: str
    MONGODB_PORT: int
    # Timeseries configurations
    BUCKET_MAX_SPAN_SECONDS: int
    BUCKET_ROUNDING_SECONDS: int
    EXPIRE_AFTER_SECONDS: int

    # Dragonfly/Redis Configurations
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None
    DEFAULT_TTL: int
    REDIS_GLOBAL_KEY_PREFIX: str

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

    @property
    def RDS_URI(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_HOST
        port = self.POSTGRES_PORT
        database = self.POSTGRES_DB
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

    @property
    def MONGO_URI(self):
        user = self.MONGODB_USER
        password = self.MONGODB_PASSWORD
        host = self.MONGODB_HOST
        port = self.MONGODB_PORT

        if user is None or password is None:
            return f"mongodb://{host}:{port}"
        return f"mongodb://{user}:{password}@{host}:{port}"

    @property
    def REDIS_URI(self) -> str:
        if not self.REDIS_PASSWORD:
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"
