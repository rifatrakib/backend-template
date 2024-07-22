from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse
from server.dependencies.authentication import authenticate_active_user
from server.dependencies.clients import get_session
from server.dependencies.requests import temporary_key
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

    @router.get(
        "/protected-check",
        response_model=MessageResponse,
        summary="Check if authentication is working",
        response_description="Authentication successful",
        dependencies=[Depends(authenticate_active_user)],
    )
    async def protected_check() -> MessageResponse:
        try:
            return await controllers.protected_check()
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
            return await controllers.register_user(request, queue, session, payload)
        except HTTPException as e:
            raise e

    @router.post(
        "/login",
        response_model=JWTResponse,
        summary="Endpoint to sign in with active user account",
        response_description="Login successful message",
    )
    async def login_active_user(
        payload: Annotated[LoginRequest, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> JWTResponse:
        try:
            return await controllers.login_active_user(session, payload)
        except HTTPException as e:
            raise e

    @router.post(
        "/openapi-login",
        include_in_schema=False,
        response_model=JWTResponse,
        summary="Endpoint only for signing in from openapi documentation pages",
        response_description="Login successful message",
    )
    async def openapi_login(
        payload: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> JWTResponse:
        try:
            return await controllers.login_active_user(session, payload)
        except HTTPException as e:
            raise e

    @router.get(
        "/activate",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Endpoint to check if account activation link is valid",
        response_description="Valid activation link message",
    )
    async def check_activation_link(key: Annotated[str, temporary_key]):
        try:
            await controllers.check_activation_link(key)
        except HTTPException as e:
            raise e

    @router.post(
        "/activate",
        response_model=MessageResponse,
        summary="Endpoint to activate user account",
        response_description="Account activation successful message",
    )
    async def activate_account(
        request: Request,
        queue: BackgroundTasks,
        key: Annotated[str, Depends(temporary_key)],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> MessageResponse:
        try:
            return await controllers.activate_account(request, queue, session, key)
        except HTTPException as e:
            raise e

    return router
