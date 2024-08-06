from fastapi import Request

from server.repositories.logs.requests import create_public_request_log


async def logging_middleware(request: Request, call_next):
    response = await call_next(request)
    await create_public_request_log(request, response)
    return response
