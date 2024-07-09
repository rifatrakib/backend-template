import os
from unittest.mock import mock_open, patch

import pytest

from server.core.config.environments import AppConfig


@pytest.fixture
def empty_env_file():
    with patch("builtins.open", mock_open(read_data="")):
        with patch.dict(os.environ, {}):
            yield


def test_app_config_initialization(empty_env_file):
    config = AppConfig(
        APP_NAME="TestApp",
        VERSION="1.0",
        API_PREFIX="/api",
        SOURCE="test",
    )
    assert config.APP_NAME == "TestApp"
    assert config.VERSION == "1.0"
    assert config.API_PREFIX == "/api"


def test_validate_api_prefix_trailing_slash(empty_env_file):
    config = AppConfig(API_PREFIX="api/")
    assert config.API_PREFIX == "/api"


def test_validate_api_prefix_no_slash(empty_env_file):
    config = AppConfig(API_PREFIX="api")
    assert config.API_PREFIX == "/api"


def test_validate_api_prefix_leading_and_trailing_slash(empty_env_file):
    config = AppConfig(API_PREFIX="/api/")
    assert config.API_PREFIX == "/api"


def test_validate_api_prefix_only_slash(empty_env_file):
    config = AppConfig(API_PREFIX="/")
    assert config.API_PREFIX == "/"


def test_validate_api_prefix_empty(empty_env_file):
    config = AppConfig(API_PREFIX="")
    assert config.API_PREFIX == "/"


def test_validate_api_prefix_multiple_slashes(empty_env_file):
    config = AppConfig(API_PREFIX="///api///")
    assert config.API_PREFIX == "/api"
