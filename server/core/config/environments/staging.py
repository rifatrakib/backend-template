from server.core.config.environments import AppConfig
from server.core.enums import Modes


class StagingConfig(AppConfig):
    MODE: Modes = Modes.STAGING
    DEBUG: bool = True
