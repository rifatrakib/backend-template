from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse
from server.dependencies.clients import get_session
from server.routes.auth.v1 import controllers
from server.schemas.requests.auth import LoginRequest, SignupRequest
from server.schemas.responses.accounts import JWTResponse


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
        response_model=MessageResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Endpoint to register new user account",
        response_description="Registration successful message",
    )
    async def register_user(
        request: Request,
        queue: BackgroundTasks,
        payload: Annotated[SignupRequest, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> MessageResponse:
        try:
            message = await controllers.register_user(request, queue, session, payload)
            return {"msg": message}
        except HTTPException as e:
            raise e

    @router.post(
        "/login",
        response_model=JWTResponse,
        summary="Endpoint to sign in with active user account",
        response_description="Login successful message",
    )
    async def login_active_user(
        queue: BackgroundTasks,
        payload: Annotated[LoginRequest, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> JWTResponse:
        try:
            return await controllers.login_active_user(session, payload)
        except HTTPException as e:
            raise e

    return router
