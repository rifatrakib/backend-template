import os
from unittest.mock import MagicMock, mock_open, patch

import pytest
import yaml

from server.core.config.sources.yaml import ConfigSource, SettingsSource


@pytest.fixture
def mock_secrets_file():
    data = {"SOURCE": "secrets.yaml"}
    with patch("pathlib.Path.is_file", return_value=True):
        with patch("pathlib.Path.open", mock_open(read_data=yaml.safe_dump(data))):
            with patch.dict(os.environ, data):
                yield


@pytest.fixture
def mock_secrets_yaml_file():
    data = {"SOURCE": "secrets.yaml"}
    with patch("pathlib.Path.is_file", return_value=True), patch("builtins.open", mock_open(read_data=yaml.safe_dump(data))), patch.dict(
        os.environ, data
    ):
        yield


def test_validate_source_valid_yaml(mock_secrets_file):
    path = "secrets.yaml"
    assert ConfigSource.validate_source(path) == path


def test_validate_source_invalid_yaml():
    with patch("pathlib.Path.is_file", return_value=True):
        with patch("yaml.safe_load", mock_open(read_data="invalid yaml content")):
            path = "secrets.yaml"
            with pytest.raises(ValueError, match="Invalid YAML file: "):
                ConfigSource.validate_source(path)


def test_validate_source_nonexistent_file():
    path = "non_existent_file.yaml"
    with pytest.raises(ValueError, match="File does not exist: non_existent_file.yaml"):
        ConfigSource.validate_source(path)


def test_read_secrets(mock_secrets_yaml_file):
    source = SettingsSource(ConfigSource)
    secrets = source.read_secrets()
    assert secrets == {"SOURCE": "secrets.yaml"}


def test_settings_source_call(mock_secrets_yaml_file):
    source = SettingsSource(ConfigSource)
    data = source()
    assert data == {"SOURCE": "secrets.yaml"}


def test_get_field_value(mock_secrets_yaml_file):
    source = SettingsSource(ConfigSource)
    _ = source()
    assert source.get_field_value("", "") is None


def test_settings_customise_sources():
    sources = ConfigSource.settings_customise_sources(
        ConfigSource,
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )
    assert len(sources) == 5
    assert isinstance(sources[-1], SettingsSource)
