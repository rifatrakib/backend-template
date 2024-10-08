from server.core.config.environments import AppConfig
from server.core.enums import Modes


class DevelopmentConfig(AppConfig):
    MODE: Modes = Modes.DEVELOPMENT
    DEBUG: bool = True
    SEND_MAIL: bool = False

    # Cache TTL settings
    ACCOUNT_ACTIVATION_TTL: int = 60
