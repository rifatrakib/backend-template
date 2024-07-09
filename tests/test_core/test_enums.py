import pytest

from server.core.enums import Modes


def test_modes_enum():
    assert Modes.DEVELOPMENT.value == "development"
    assert Modes.STAGING.value == "staging"
    assert Modes.PRODUCTION.value == "production"

    assert Modes("development") == Modes.DEVELOPMENT
    assert Modes("staging") == Modes.STAGING
    assert Modes("production") == Modes.PRODUCTION

    with pytest.raises(ValueError):
        Modes("invalid")
