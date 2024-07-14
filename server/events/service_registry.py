import asyncio
from pathlib import Path
from types import ModuleType

import aiofiles
from fastapi import FastAPI
from starlette.routing import BaseRoute

from server.core.config import settings
from server.core.enums import Tags, Versions


async def add_endpoint_description(route: BaseRoute, python_path: str, version: str) -> None:
    directory = python_path.replace(".", "/")
    # documentation is stored in a markdown file (can be generated using CLI)
    # with the same name as the endpoint handler function name
    # in a folder named after the version of the API inside the `docs` folder of the service
    async with aiofiles.open(f"{directory}/docs/{version}/{route.name}.md") as reader:
        description = await reader.read()

    # Enforce that the description is not empty
    if not description.strip():
        raise ValueError(f"Description for {route.name} in {python_path} is empty")

    route.description = description


def validate_tags(route: BaseRoute) -> None:
    if not all(item in enum_class.__members__.values() for enum_class in [Tags, Versions] for item in route.tags):
        raise ValueError(f"Invalid tags in {route.name} in {route.path}. Please use the Tags and Versions enums for tags")


def find_services() -> list[ModuleType]:
    # all the services are stored in the `server/routes` folder
    services = []
    for item in Path("server/routes").iterdir():
        if item.is_dir() and item.name != "__pycache__":
            # import the module dynamically
            module = __import__(f"server.routes.{item.name}", fromlist=[""])
            services.append(module)

    return services


async def register_routers(app: FastAPI) -> FastAPI:
    services = find_services()
    tasks = []

    for service in services:
        # Invoke the common `create_router()` function in each module to get an APIRouter instance
        router = service.create_router()

        for route in router.routes:
            validate_tags(route)
            # the version number is the second part of the path (e.g. /api/v1/...)
            route_version = route.path.split("/")[1]
            tasks.append(add_endpoint_description(route, service.__name__, route_version))

        await asyncio.gather(*tasks, return_exceptions=True)
        app.include_router(router, prefix=settings.API_PREFIX)
        tasks = []

    return app
