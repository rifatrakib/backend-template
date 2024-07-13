from pathlib import Path
from types import ModuleType

from fastapi import FastAPI
from starlette.routing import BaseRoute

from server.core.config import settings


# TODO: Read files asynchronously with `aiofiles` later
def add_endpoint_description(route: BaseRoute, python_path: str, version: str) -> None:
    directory = python_path.replace(".", "/")
    # documentation is stored in a markdown file (can be generated using CLI)
    # with the same name as the endpoint handler function name
    # in a folder named after the version of the API inside the `docs` folder of the service
    with open(f"{directory}/docs/{version}/{route.name}.md") as reader:
        route.description = reader.read()


def find_services() -> list[ModuleType]:
    # all the services are stored in the `server/routes` folder
    services = []
    for item in Path("server/routes").iterdir():
        if item.is_dir() and item.name != "__pycache__":
            # import the module dynamically
            module = __import__(f"server.routes.{item.name}", fromlist=[""])
            services.append(module)

    return services


# TODO: Make this function async after integrating it with lifespan function
def register_routers(app: FastAPI) -> FastAPI:
    services = find_services()

    for service in services:
        # Invoke the common `create_router()` function in each module to get an APIRouter instance
        router = service.create_router()

        for route in router.routes:
            # the version number is the second part of the path (e.g. /api/v1/...)
            route_version = route.path.split("/")[1]
            add_endpoint_description(route, service.__name__, route_version)

        app.include_router(router, prefix=settings.API_PREFIX)

    return app
