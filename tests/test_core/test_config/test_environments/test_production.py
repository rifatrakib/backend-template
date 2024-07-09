from server.core.config.environments.production import ProductionConfig
from server.core.enums import Modes


def test_production_config_initialization():
    config = ProductionConfig(
        APP_NAME="TestApp",
        MODE=Modes.PRODUCTION,
        VERSION="1.0",
        API_PREFIX="/api",
    )

    # Check inherited attributes
    assert config.APP_NAME == "TestApp"
    assert config.MODE == Modes.PRODUCTION
    assert config.VERSION == "1.0"
    assert config.API_PREFIX == "/api"

    # Check DevelopmentConfig specific attributes
    assert config.DEBUG is False
    assert config.MODE == "production"
