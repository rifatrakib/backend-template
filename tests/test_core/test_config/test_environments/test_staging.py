from server.core.config.environments.staging import StagingConfig
from server.core.enums import Modes


def test_staging_config_initialization():
    config = StagingConfig(
        APP_NAME="TestApp",
        MODE=Modes.STAGING,
        VERSION="1.0",
        API_PREFIX="/api",
        TERMS_OF_SERVICE="https://example.com",
        MAINTAINER_NAME="Test Maintainer",
        MAINTAINER_ONLINE_PROFILE="https://example.com",
        MAINTAINER_EMAIL="admin@example.com",
    )

    # Check inherited attributes
    assert config.APP_NAME == "TestApp"
    assert config.MODE == Modes.STAGING
    assert config.VERSION == "1.0"
    assert config.API_PREFIX == "/api"

    # Check DevelopmentConfig specific attributes
    assert config.DEBUG is True
    assert config.MODE == "staging"
