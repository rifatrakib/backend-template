from typing import Annotated

from fastapi import APIRouter, Depends

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse
from server.dependencies.form import signup_form
from server.schemas.requests.auth import SignupRequest


def create_router():
    router = APIRouter(
        prefix="/auth",
        tags=[Tags.AUTHENTICATION],
    )

    @router.get(
        "/check",
        summary="Check if the auth service is up and running",
        response_description="Auth service status",
        tags=[Tags.HEALTH_CHECK],
        response_model=MessageResponse,
    )
    async def check_auth_service():
        return {"msg": "Auth service is up and running!"}

    @router.post(
        "/signup",
        summary="Endpoint to register new user account",
        response_description="Registration successful message",
    )
    async def register_user(payload: Annotated[SignupRequest, Depends(signup_form)]):
        return payload

    return router
