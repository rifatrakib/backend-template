from pydantic import Field

from server.core.schemas import BaseResponseSchema


class ValidationResponse(BaseResponseSchema):
    is_valid: bool = Field(..., description="Whether the entity is valid and available.")
    prompt: str = Field(..., description="Prompt message for the client-side.")
