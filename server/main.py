from fastapi import FastAPI

from server.core.documentation.openapi import configure_openapi
from server.core.schemas.utilities import OpenAPIConfig
from server.events.service_registry import register_routers


def configure_app() -> FastAPI:
    api_config: OpenAPIConfig = configure_openapi()
    app = FastAPI(**api_config.model_dump())
    register_routers(app)
    return app


app: FastAPI = configure_app()
