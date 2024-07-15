import subprocess
from contextlib import asynccontextmanager

from aredis_om import Migrator
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from server.core.config import settings
from server.core.models.mongodb.accounts import AccountCache
from server.events.service_registry import register_routers
from server.schemas.requests.auth import SignupRequest


async def run_migrations():
    subprocess.run("alembic upgrade head", shell=True)


def customize_form_data(app: FastAPI):
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
        client = AsyncIOMotorClient(settings.MONGO_URI)
        await init_beanie(
            database=client["test"],
            document_models=[AccountCache],
        )

        # Connect to Redis
        await Migrator().run()

    yield
