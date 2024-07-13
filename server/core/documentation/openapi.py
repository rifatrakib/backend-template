from pathlib import Path

from server.core.config import settings
from server.core.enums import Tags
from server.core.schemas.utilities import APIConfig, Contact, ExternalDocs, OpenAPIConfig, OpenAPITags
from server.core.utils import validate_file


def api_configuration_options() -> APIConfig:
    try:
        with open(validate_file(Path("server/README.md"), ["md"])) as reader:
            description = reader.read()

        api_config = APIConfig(
            title=settings.APP_NAME,
            description=description,
            version=settings.VERSION,
            terms_of_service=str(settings.TERMS_OF_SERVICE),
            contact=Contact(
                name=settings.MAINTAINER_NAME,
                url=settings.MAINTAINER_ONLINE_PROFILE,
                email=settings.MAINTAINER_EMAIL,
            ),
            openapi_url=f"{settings.API_PREFIX}/openapi.json",
            docs_url=f"{settings.API_PREFIX}/docs",
            redoc_url=f"{settings.API_PREFIX}/redoc",
        )
        return api_config
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error occurred while configuring the API: {e}")


def configure_openapi() -> OpenAPIConfig:
    api_config: APIConfig = api_configuration_options()
    tags_metadata: list[OpenAPITags] = [
        OpenAPITags(
            name=Tags.HEALTH_CHECK,
            description="Verify server operability and configuration variables.",
            external_docs=ExternalDocs(
                description="Server Health Check",
                url="https://example.com/",
            ),
        ),
    ]
    return OpenAPIConfig(**api_config.model_dump(), tags_metadata=tags_metadata)
