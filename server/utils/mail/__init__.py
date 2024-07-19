from functools import lru_cache
from typing import Any

from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from server.core.config import settings


@lru_cache()
def config_smtp_server() -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=settings.USE_CREDENTIALS,
    )


@lru_cache()
def config_templates() -> Jinja2Templates:
    return Jinja2Templates(directory="server/utils/mail/templates")


def build_mail_body(context: dict[str, Any], template_name: str) -> str:
    template_server: Jinja2Templates = config_templates()
    template = template_server.TemplateResponse(name=template_name, context=context)
    return template.body.decode("utf-8")


def prepare_message(context: dict[str, Any], recipients: list[EmailStr], template_name: str) -> MessageSchema:
    return MessageSchema(
        subject=context["subject"],
        recipients=recipients,
        body=build_mail_body(context, template_name),
        subtype=MessageType.html,
    )


async def send_mail(context: dict[str, Any], recipients: list[EmailStr], template_name: str) -> None:
    smtp_config: ConnectionConfig = config_smtp_server()
    smtp_agent = FastMail(smtp_config)
    message: MessageSchema = prepare_message(context, recipients, template_name)
    await smtp_agent.send_message(message)
