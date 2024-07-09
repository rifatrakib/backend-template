from server.core.config.environments import AppConfig
from server.core.enums import Modes


class ProductionConfig(AppConfig):
    MODE: Modes = Modes.PRODUCTION
    DEBUG: bool = False
