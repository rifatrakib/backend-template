from datetime import timedelta

from server.core.config.environments import AppConfig
from server.core.enums import Modes


class StagingConfig(AppConfig):
    MODE: Modes = Modes.STAGING
    DEBUG: bool = True

    # Cache TTL settings
    ACCOUNT_ACTIVATION_TTL: int = timedelta(minutes=60).seconds
