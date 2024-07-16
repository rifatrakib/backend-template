from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse
from server.dependencies.form import signup_form
from server.routes.auth.v1 import controllers
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
    async def check_auth_service() -> MessageResponse:
        try:
            return await controllers.check_auth_service()
        except HTTPException as e:
            raise e

    @router.post(
        "/signup",
        summary="Endpoint to register new user account",
        response_description="Registration successful message",
    )
    async def register_user(payload: Annotated[SignupRequest, Depends(signup_form)]):
        try:
            return await controllers.register_user(payload)
        except HTTPException as e:
            raise e

    return router
