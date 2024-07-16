from fastapi import APIRouter, HTTPException

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse
from server.routes.health.v1 import controllers


def create_router():
    router = APIRouter(
        prefix="/health",
        tags=[Tags.HEALTH_CHECK],
    )

    @router.get(
        "",
        summary="Check if the application is up and running",
        response_description="Application health check",
        response_model=MessageResponse,
    )
    async def check_health_service():
        try:
            return await controllers.check_health_service()
        except HTTPException as e:
            raise e

    return router
