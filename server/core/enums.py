from enum import Enum


class Modes(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Tags(str, Enum):
    HEALTH_CHECK = "Health Check"
