from enum import Enum


class EnvSources(str, Enum):
    DOTENV = ".env"
    JSON = "json"
    YAML = "yaml"


class Databases(str, Enum):
    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"
    REDIS = "redis"


class Modes(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Tags(str, Enum):
    HEALTH_CHECK = "Health Check"
    AUTHENTICATION = "Authentication"
    VALIDATION = "Validation"


class Versions(str, Enum):
    VERSION_1 = "Version 1"


class Providers(str, Enum):
    GOOGLE = "google"
    GITHUB = "github"


class Genders(str, Enum):
    MALE = "m"
    FEMALE = "f"
