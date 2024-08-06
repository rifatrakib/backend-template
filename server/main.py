from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.core.documentation.openapi import configure_openapi
from server.core.schemas.utilities import OpenAPIConfig
from server.events.startup import app_startup
from server.middlewares.logging import logging_middleware


def configure_app() -> FastAPI:
    api_config: OpenAPIConfig = configure_openapi()
    app = FastAPI(**api_config.model_dump(), lifespan=app_startup)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware("http")(logging_middleware)
    return app


app: FastAPI = configure_app()
