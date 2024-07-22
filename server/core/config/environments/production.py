from datetime import timedelta

from server.core.config.environments import AppConfig
from server.core.enums import Modes


class ProductionConfig(AppConfig):
    MODE: Modes = Modes.PRODUCTION
    DEBUG: bool = False

    # Cache TTL settings
    ACCOUNT_ACTIVATION_TTL: int = timedelta(days=1).seconds
