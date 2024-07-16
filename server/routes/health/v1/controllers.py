from server.core.schemas.utilities import MessageResponse


async def check_health_service() -> MessageResponse:
    return MessageResponse(msg="Health service is up and running!")
