import os
from unittest.mock import patch

import pytest

from server.core.config import SettingsFactory, get_settings
from server.core.config.environments.development import DevelopmentConfig
from server.core.config.environments.production import ProductionConfig
from server.core.config.environments.staging import StagingConfig
from server.core.enums import Modes


@pytest.fixture
def mock_os_environ():
    with patch.dict(os.environ, {}, clear=True):
        yield


def test_settings_factory_initialization():
    factory = SettingsFactory(mode=Modes.DEVELOPMENT)
    assert factory.mode == Modes.DEVELOPMENT

    factory = SettingsFactory(mode=Modes.STAGING)
    assert factory.mode == Modes.STAGING

    factory = SettingsFactory(mode=Modes.PRODUCTION)
    assert factory.mode == Modes.PRODUCTION


def test_settings_factory_call_development(mock_os_environ):
    factory = SettingsFactory(mode=Modes.DEVELOPMENT)
    config = factory()
    assert isinstance(config, DevelopmentConfig)


def test_settings_factory_call_staging(mock_os_environ):
    factory = SettingsFactory(mode=Modes.STAGING)
    config = factory()
    assert isinstance(config, StagingConfig)


def test_settings_factory_call_production(mock_os_environ):
    factory = SettingsFactory(mode=Modes.PRODUCTION)
    config = factory()
    assert isinstance(config, ProductionConfig)


def test_get_settings_development(mock_os_environ):
    settings = get_settings(Modes.DEVELOPMENT)
    assert isinstance(settings, DevelopmentConfig)


def test_get_settings_staging(mock_os_environ):
    settings = get_settings(Modes.STAGING)
    assert isinstance(settings, StagingConfig)


def test_get_settings_production(mock_os_environ):
    settings = get_settings(Modes.PRODUCTION)
    assert isinstance(settings, ProductionConfig)


def test_get_settings_cached(mock_os_environ):
    settings1 = get_settings(Modes.DEVELOPMENT)
    settings2 = get_settings(Modes.DEVELOPMENT)
    assert settings1 is settings2
