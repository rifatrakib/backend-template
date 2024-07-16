from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.enums import Tags
from server.core.schemas.utilities import MessageResponse
from server.dependencies.clients import get_session
from server.dependencies.fields import email_field
from server.repositories.auth.read import get_account_by_email
from server.schemas.responses.validation import ValidationResponse


def create_router():
    router = APIRouter(
        prefix="/validate",
        tags=[Tags.VALIDATION],
    )

    @router.get(
        "/check",
        summary="Check if the validation service is up and running",
        response_description="Validation service status",
        tags=[Tags.HEALTH_CHECK],
        response_model=MessageResponse,
    )
    async def check_validation_service():
        return {"msg": "Validation service is up and running!"}

    @router.get(
        "/accounts/email",
        response_model=ValidationResponse,
        summary="Validate if the email is available to be used for signup.",
        response_description="Availability of email address.",
    )
    async def validate_email(
        email: Annotated[EmailStr, email_field(Query, alias="q")],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> ValidationResponse:
        try:
            account = await get_account_by_email(session, email)
            return {
                "is_valid": account is None,
                "prompt": "Email is available for signup.",
            }
        except HTTPException as e:
            raise e

    return router
