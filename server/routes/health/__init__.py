from fastapi import APIRouter

from server.routes.health import v1


def create_router():
    # Not using versioning as this is the health route and it should be the same for all versions
    router = APIRouter()

    router.include_router(v1.create_router())

    return router
