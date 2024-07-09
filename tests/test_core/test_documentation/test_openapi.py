from unittest.mock import MagicMock, mock_open, patch

import pytest
from starlette.routing import BaseRoute

from server.core.config import settings
from server.core.documentation.openapi import add_endpoint_description, api_configuration_options, configure_openapi
from server.core.documentation.schemas import APIConfig, ExternalDocs, OpenAPIConfig, OpenAPITags
from server.core.enums import Tags


def test_api_configuration_options():
    mock_description = "Test description from README.md"
    with patch("builtins.open", mock_open(read_data=mock_description)):
        api_config = api_configuration_options()

    assert isinstance(api_config, APIConfig)
    assert api_config.title == settings.APP_NAME
    assert api_config.description == mock_description
    assert api_config.version == settings.VERSION
    assert str(api_config.terms_of_service) == "https://example.com/terms-of-services"
    assert api_config.openapi_url == f"{settings.API_PREFIX}/openapi.json"
    assert api_config.docs_url == f"{settings.API_PREFIX}/docs"
    assert api_config.redoc_url == f"{settings.API_PREFIX}/redoc"


def test_api_configuration_options_fail():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("server.core.utils.validate_file", return_value="server/non-existant-file.md"):
            with pytest.raises(FileNotFoundError, match="Error occurred while configuring the API: "):
                api_configuration_options()


def test_configure_openapi():
    mock_description = "Test description from README.md"
    expected_tags_metadata = [
        OpenAPITags(
            name=Tags.HEALTH_CHECK,
            description="Verify server operability and configuration variables.",
            externalDocs=ExternalDocs(
                description="Server Health Check",
                url="https://example.com/",
            ),
        ),
    ]

    with patch("builtins.open", mock_open(read_data=mock_description)):
        openapi_config = configure_openapi()

    assert isinstance(openapi_config, OpenAPIConfig)
    assert openapi_config.title == settings.APP_NAME
    assert openapi_config.description == mock_description
    assert openapi_config.version == settings.VERSION
    assert str(openapi_config.terms_of_service) == "https://example.com/terms-of-services"
    assert openapi_config.openapi_url == f"{settings.API_PREFIX}/openapi.json"
    assert openapi_config.docs_url == f"{settings.API_PREFIX}/docs"
    assert openapi_config.redoc_url == f"{settings.API_PREFIX}/redoc"
    assert openapi_config.tags_metadata == expected_tags_metadata


def test_add_endpoint_description():
    # Mock route
    mock_route = MagicMock(spec=BaseRoute)
    mock_route.name = "test_endpoint"

    # Mock the open function to simulate reading from a file
    mock_description = "This is a test description."
    with patch("builtins.open", mock_open(read_data=mock_description)):

        # Call the function with the mocked route and python_path
        add_endpoint_description(mock_route, "server.core.api")

        # Check if the route's description was set correctly
        assert mock_route.description == mock_description


def test_add_endpoint_description_invalid_path():
    # Mock route
    mock_route = MagicMock(spec=BaseRoute)
    mock_route.name = "test_endpoint"

    # Mock the open function to raise a FileNotFoundError
    with patch("builtins.open", side_effect=FileNotFoundError):

        # Call the function with the mocked route and python_path
        with pytest.raises(FileNotFoundError):
            add_endpoint_description(mock_route, "server.core.api")
