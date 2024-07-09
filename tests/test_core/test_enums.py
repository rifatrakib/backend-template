import pytest

from server.core.enums import Modes, Tags


def test_modes_enum():
    assert Modes.DEVELOPMENT.value == "development"
    assert Modes.STAGING.value == "staging"
    assert Modes.PRODUCTION.value == "production"

    assert Modes("development") == Modes.DEVELOPMENT
    assert Modes("staging") == Modes.STAGING
    assert Modes("production") == Modes.PRODUCTION

    with pytest.raises(ValueError):
        Modes("invalid")


def test_tags_enum():
    assert Tags.HEALTH_CHECK.value == "Health Check"
    with pytest.raises(ValueError):
        Tags("INVALID")
