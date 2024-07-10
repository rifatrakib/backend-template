from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import Column, String, event

from server.core.models.sql import Base


class ExampleModel(Base):
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


@pytest.fixture
def mock_session():
    with patch("sqlalchemy.orm.Session") as mock_session:
        yield mock_session


def test_table_name():
    assert ExampleModel.__tablename__ == "example_models"


def test_create_example_model(mock_session):
    mock_session_instance = mock_session.return_value
    mock_session_instance.commit = MagicMock()

    example = ExampleModel(name="Test Example", description="This is a test example.", creator_id=1, last_updator_id=1, deletor_id=1)
    example.id = 1
    example.created_at = datetime.now()
    example.revision_id = 1

    mock_session_instance.add(example)
    mock_session_instance.commit()

    assert example.id == 1  # Explicitly set in the test
    assert example.created_at is not None  # Explicitly set in the test
    assert example.revision_id == 1
    assert str(example) == "<ExampleModel(id=1)>"


def test_relationships(mock_session):
    mock_session_instance = mock_session.return_value
    mock_session_instance.commit = MagicMock()

    example = ExampleModel(name="Test Example", description="This is a test example.", creator_id=1, last_updator_id=1, deletor_id=1)

    mock_session_instance.add(example)
    mock_session_instance.commit()

    assert example.created_by is None  # Relationships will not be set in a mock
    assert example.last_updated_by is None
    assert example.deleted_by is None


def test_revision_increment(mock_session):
    mock_session_instance = mock_session.return_value
    mock_session_instance.commit = MagicMock()

    example = ExampleModel(name="Test Example", description="This is a test example.", creator_id=1, last_updator_id=1, deletor_id=1)
    example.id = 1
    example.revision_id = 1

    original_revision = example.revision_id
    example.name = "Updated Example"

    event.listen(ExampleModel, "before_update", Base._increment_revision_id)

    mock_session_instance.add(example)
    mock_session_instance.commit()

    # Manually trigger the before_update event to increment the revision_id
    Base._increment_revision_id(None, None, example)

    assert example.revision_id == original_revision + 1
