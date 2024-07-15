from fastapi import APIRouter

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse


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
        return {"msg": "The application is up and running!"}

    return router
