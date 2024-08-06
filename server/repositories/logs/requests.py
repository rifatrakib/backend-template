from fastapi import Request, Response

from server.core.config import settings
from server.models.mongodb.events import RequestLog


async def create_public_request_log(request: Request, response: Response, body: dict | list | None = None):
    log = RequestLog(
        endpoint=request.url.path,
        method=request.method,
        query_params=dict(request.query_params),
        request_body=body,
        headers=dict(request.headers),
        status_code=response.status_code,
        client_ip=request.client.host,
        metadata={
            "environment": settings.MODE,
            "source": request.headers.get("x-forwarded-for", request.client.host),
        },
    )
    await log.save()
