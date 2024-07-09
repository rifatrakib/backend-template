import json
import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from server.core.config.sources.json import ConfigSource, SettingsSource


@pytest.fixture
def mock_secrets_file():
    data = {"SOURCE": "secrets.json"}
    with patch("pathlib.Path.is_file", return_value=True):
        with patch("pathlib.Path.open", mock_open(read_data=json.dumps(data))):
            with patch.dict(os.environ, data):
                yield


@pytest.fixture
def mock_secrets_json_file():
    data = {"SOURCE": "secrets.json"}
    with patch("pathlib.Path.is_file", return_value=True), patch("builtins.open", mock_open(read_data=json.dumps(data))), patch.dict(
        os.environ, data
    ):
        yield


def test_validate_source_valid_json(mock_secrets_file):
    path = "secrets.json"
    assert ConfigSource.validate_source(path) == path


def test_validate_source_invalid_json():
    with patch("pathlib.Path.is_file", return_value=True):
        with patch("pathlib.Path.open", mock_open(read_data="invalid json content")):
            path = "secrets.json"
            with pytest.raises(ValueError, match="Invalid JSON file: "):
                ConfigSource.validate_source(path)


def test_validate_source_nonexistent_file():
    path = "non_existent_file.json"
    with pytest.raises(ValueError, match="File does not exist: non_existent_file.json"):
        ConfigSource.validate_source(path)


def test_read_secrets(mock_secrets_json_file):
    source = SettingsSource(ConfigSource)
    secrets = source.read_secrets()
    assert secrets == {"SOURCE": "secrets.json"}


def test_settings_source_call(mock_secrets_json_file):
    source = SettingsSource(ConfigSource)
    data = source()
    assert data == {"SOURCE": "secrets.json"}


def test_get_field_value(mock_secrets_json_file):
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
