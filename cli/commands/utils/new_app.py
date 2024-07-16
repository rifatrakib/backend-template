from pathlib import Path

from server.core.config import settings


def init_file_contents(name: str) -> str:
    contents = f"""from fastapi import APIRouter

from server.core.enums import Versions
from server.routes.{name} import v1


def create_router():
    router = APIRouter(prefix="/v1", tags=[Versions.VERSION_1])

    router.include_router(v1.create_router())

    return router
"""

    return contents


def v1_file_contents(name: str) -> str:
    contents = f"""from fastapi import APIRouter, HTTPException

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse
from server.routes.{name}.v1 import controllers


def create_router():
    router = APIRouter(
        prefix="/{name}",
        tags=["{name}"],  # TODO: Suggestion - Use the Tags enum class in the server.core.enums module
    )

    @router.get(
        "/check",
        summary="Check if the {name} service is up and running",
        response_description="{name.capitalize()} service status",
        tags=[Tags.HEALTH_CHECK],
        response_model=MessageResponse,
    )
    async def check_{name}_service() -> MessageResponse:
        try:
            return await controllers.check_{name}_service()
        except HTTPException as e:
            raise e

    return router
"""

    return contents


def controller_file_contents(name: str) -> str:
    contents = f"""from server.core.schemas.utilities import MessageResponse


async def check_{name}_service() -> MessageResponse:
    return MessageResponse(msg="{name.capitalize()} service is up and running!")
"""

    return contents


def check_route_doc_contents(name: str) -> str:
    with open("cli/commands/templates/new-app-check.md") as f:
        contents = f.read()

    contents = contents.replace("{Name}", name.capitalize())
    contents = contents.replace("{name}", name)
    contents = contents.replace("/{api_prefix}", settings.API_PREFIX)

    return contents


def make_new_app_files(name: str, directory: Path) -> None:
    # Create the __init__.py file
    init_file = Path(f"{directory}/__init__.py")

    init_file.write_text(init_file_contents(name))

    # Create the v1 directory for the first version of the app routes
    v1_directory = Path(f"{directory}/v1")
    v1_directory.mkdir(parents=True, exist_ok=True)
    v1_file = Path(f"{v1_directory}/__init__.py")
    v1_file.write_text(v1_file_contents(name))
    controller_file = Path(f"{v1_directory}/controllers.py")
    controller_file.write_text(controller_file_contents(name))

    # Create the docs directory for the first version of the app routes
    docs_directory = Path(f"{v1_directory}/docs")
    docs_directory.mkdir(parents=True, exist_ok=True)
    check_doc_file = Path(f"{docs_directory}/check_{name}_service.md")
    check_doc_file.write_text(check_route_doc_contents(name))


def is_valid_service(name: str) -> bool:
    directory = Path(f"server/routes/{name}")
    return not directory.exists()
