from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse
from server.dependencies.clients import get_session
from server.dependencies.form import signup_form
from server.routes.auth.v1 import controllers
from server.schemas.requests.auth import SignupRequest
from server.schemas.responses.accounts import AccountResponse


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
        response_model=AccountResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Endpoint to register new user account",
        response_description="Registration successful message",
    )
    async def register_user(
        session: Annotated[AsyncSession, Depends(get_session)],
        payload: Annotated[SignupRequest, Depends(signup_form)],
    ) -> AccountResponse:
        try:
            return await controllers.register_user(session, payload)
        except HTTPException as e:
            raise e

    return router
