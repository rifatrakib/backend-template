from contextlib import asynccontextmanager

from aredis_om import Migrator
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from server.core.config import settings
from server.core.models.mongodb.accounts import AccountCache


@asynccontextmanager
async def app_startup(app: FastAPI):
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client["test"],
        document_models=[AccountCache],
    )

    # Connect to Redis
    await Migrator().run()

    yield
