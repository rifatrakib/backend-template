import os
from unittest.mock import mock_open, patch

import pytest

from server.core.config.sources import ConfigSource
from server.core.schemas import BaseConfig


@pytest.fixture
def empty_env_file():
    with patch("builtins.open", mock_open(read_data="")):
        with patch.dict(os.environ, {}):
            yield


def test_config_source(empty_env_file):
    source = ConfigSource()
    assert source.SOURCE == ".env"
    assert source.model_config.get("env_file_encoding") == "utf-8"
    assert source.model_config.get("env_file") == ".env"
    assert source.model_config.get("extra") == "forbid"
    assert isinstance(source, ConfigSource)
    assert isinstance(source, BaseConfig)
