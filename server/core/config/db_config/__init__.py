import os
from typing import Type

from server.core.config.db_config import mongodb, postgresql, redis
from server.core.enums import Databases


def configure_db_config() -> list[Type]:
    databases = os.environ.get("DATABASES", "").split(",")
    classes = []

    if Databases.MONGODB in databases:
        classes.append(mongodb.Config)
    if Databases.POSTGRESQL in databases:
        classes.append(postgresql.Config)
    if Databases.REDIS in databases:
        classes.append(redis.Config)

    return classes


class DatabaseConfig(*configure_db_config()):
    DATABASES: str
