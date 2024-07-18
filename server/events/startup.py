import subprocess
from contextlib import asynccontextmanager
from typing import Type

from aredis_om import Migrator
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from server.core.config import settings
from server.core.models.mongodb.accounts import AccountCache
from server.events.service_registry import register_routers
from server.models.mongodb.events import ChangeLog, RequestLog
from server.schemas.requests.auth import SignupRequest


async def run_migrations() -> None:
    subprocess.run("alembic upgrade head", shell=True)


def mongodb_collections() -> list[Type]:
    return [
        AccountCache,
        ChangeLog,
        RequestLog,
    ]


async def initialize_mongodb() -> None:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    targets = {}
    for collection in mongodb_collections():
        database = collection.__module__.split(".")[-1]
        if database not in targets:
            targets[database] = {"database": client[database], "document_models": []}
        targets[database]["document_models"].append(collection)

    for target in targets.values():
        await init_beanie(**target)


def customize_form_data(app: FastAPI) -> None:
    openapi_schema = app.openapi()
    schemas = openapi_schema["components"]["schemas"]

    # Add examples to the form fields for the signup endpoint
    SignupRequest.form_example(schemas["Body_register_user_api_v1_auth_signup_post"]["properties"])


@asynccontextmanager
async def app_startup(app: FastAPI):
    # Register routers for all the services
    await register_routers(app)
    customize_form_data(app)

    if not settings.TEST_RUN:
        # Migrate the database
        await run_migrations()

        # Connect to MongoDB
        await initialize_mongodb()

        # Connect to Redis
        await Migrator().run()

    yield
