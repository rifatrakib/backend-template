from server.core.schemas.utilities import MessageResponse
from server.schemas.requests.auth import SignupRequest


async def check_auth_service() -> MessageResponse:
    return MessageResponse(msg="Auth service is up and running!")


async def register_user(payload: SignupRequest) -> SignupRequest:
    return payload
