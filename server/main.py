from fastapi import FastAPI

from server.core.documentation.openapi import configure_openapi
from server.core.schemas.utilities import OpenAPIConfig
from server.events.startup import app_startup


def configure_app() -> FastAPI:
    api_config: OpenAPIConfig = configure_openapi()
    app = FastAPI(**api_config.model_dump(), lifespan=app_startup)
    return app


app: FastAPI = configure_app()
