from server.core.documentation.schemas import APIConfig, Contact, ExternalDocs, OpenAPIConfig, OpenAPITags


def test_contact_schema():
    contact_data = {"name": "API Support", "url": "http://example.com/support", "email": "support@example.com"}

    contact = Contact(**contact_data)

    assert contact.name == "API Support"
    assert str(contact.url) == "http://example.com/support"
    assert contact.email == "support@example.com"


def test_api_config_schema():
    contact_data = Contact(name="API Support", url="http://example.com/support", email="support@example.com")
    api_config_data = {
        "title": "My API",
        "description": "API Description",
        "version": "1.0",
        "terms_of_service": "https://example.com/terms/",
        "contact": contact_data.model_dump(),
        "openapi_url": "/openapi.json",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }

    api_config = APIConfig(**api_config_data)

    assert api_config.title == "My API"
    assert api_config.description == "API Description"
    assert api_config.version == "1.0"
    assert str(api_config.terms_of_service) == "https://example.com/terms/"
    assert api_config.contact == contact_data
    assert api_config.openapi_url == "/openapi.json"
    assert api_config.docs_url == "/docs"
    assert api_config.redoc_url == "/redoc"


def test_external_docs_schema():
    external_docs_data = {"description": "External Documentation", "url": "http://example.com/external"}

    external_docs = ExternalDocs(**external_docs_data)

    assert external_docs.description == "External Documentation"
    assert str(external_docs.url) == "http://example.com/external"


def test_openapi_tags_schema():
    external_docs_data = ExternalDocs(description="External Documentation", url="http://example.com/external")
    openapi_tags_data = {"name": "health", "description": "Health Check API", "externalDocs": external_docs_data.model_dump()}

    openapi_tags = OpenAPITags(**openapi_tags_data)

    assert openapi_tags.name == "health"
    assert openapi_tags.description == "Health Check API"
    assert openapi_tags.external_docs == external_docs_data


def test_openapi_config_schema():
    contact_data = Contact(name="API Support", url="http://example.com/support", email="support@example.com")
    external_docs_data = ExternalDocs(description="External Documentation", url="http://example.com/external")
    openapi_tags_data = OpenAPITags(name="health", description="Health Check API", externalDocs=external_docs_data)

    openapi_config_data = {
        "title": "My API",
        "description": "API Description",
        "version": "1.0",
        "terms_of_service": "https://example.com/terms/",
        "contact": contact_data.model_dump(),
        "openapi_url": "/openapi.json",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "tags_metadata": [openapi_tags_data.model_dump()],
    }

    openapi_config = OpenAPIConfig(**openapi_config_data)

    assert openapi_config.title == "My API"
    assert openapi_config.description == "API Description"
    assert openapi_config.version == "1.0"
    assert str(openapi_config.terms_of_service) == "https://example.com/terms/"
    assert openapi_config.contact == contact_data
    assert openapi_config.openapi_url == "/openapi.json"
    assert openapi_config.docs_url == "/docs"
    assert openapi_config.redoc_url == "/redoc"
    assert openapi_config.tags_metadata == [openapi_tags_data]
