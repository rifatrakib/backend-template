from fastapi import APIRouter

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse


def create_router():
    router = APIRouter(
        prefix="/health",
        tags=[Tags.HEALTH_CHECK],
    )

    @router.get(
        "/check",
        summary="Check if the health service is up and running",
        response_description="Health service status",
        response_model=MessageResponse,
    )
    async def check_health_service():
        return {"msg": "Health service is up and running!"}

    return router
