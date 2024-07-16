from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from server.repositories.auth.read import get_account_by_email
from server.schemas.responses.validation import ValidationResponse


async def validate_email_controller(session: AsyncSession, email: EmailStr) -> ValidationResponse:
    try:
        account = await get_account_by_email(session, email)
        return ValidationResponse(
            is_valid=account is None,
            prompt="Email is available for signup." if account is None else "Email is already in use.",
        )
    except HTTPException as e:
        raise e
