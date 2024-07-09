from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from server.core.utils import validate_file


def test_validate_file_with_valid_extension():
    with NamedTemporaryFile(suffix=".json") as tmp:
        path = Path(tmp.name)
        extensions = ["json"]
        assert validate_file(path, extensions) == path


def test_validate_file_with_invalid_extension():
    with NamedTemporaryFile(suffix=".xml") as tmp:
        path = Path(tmp.name)
        extensions = ["json"]
        with pytest.raises(ValueError, match="Source file must be a json file"):
            validate_file(path, extensions)


def test_validate_file_non_existent():
    path = Path("non_existent_file.json")
    extensions = ["json"]
    with pytest.raises(ValueError, match=f"File does not exist: {path}"):
        validate_file(path, extensions)


def test_validate_file_with_multiple_extensions():
    with NamedTemporaryFile(suffix=".yml") as tmp:
        path = Path(tmp.name)
        extensions = ["yaml", "yml"]
        assert validate_file(path, extensions) == path


def test_validate_file_case_insensitive_extension():
    with NamedTemporaryFile(suffix=".JSON") as tmp:
        path = Path(tmp.name)
        extensions = ["json"]
        assert validate_file(path, extensions) == path
