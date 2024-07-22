from typing import Annotated

from fastapi import Query


def temporary_key(key: Annotated[str, Query(..., description="Temporary link key with an expiry")]) -> str:
    return key
