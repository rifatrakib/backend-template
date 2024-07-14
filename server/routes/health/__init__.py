from fastapi import APIRouter

from server.core.enums import Versions
from server.routes.health import v1


def create_router():
    router = APIRouter(prefix="/v1", tags=[Versions.VERSION_1])

    router.include_router(v1.create_router())

    return router
