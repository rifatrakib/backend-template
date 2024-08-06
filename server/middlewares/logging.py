from json.decoder import JSONDecodeError

from fastapi import Request

from server.repositories.logs.requests import create_public_request_log


async def logging_middleware(request: Request, call_next):
    try:
        body = await request.json()
    except JSONDecodeError:
        body = None

    response = await call_next(request)
    await create_public_request_log(request, response, body)
    return response
