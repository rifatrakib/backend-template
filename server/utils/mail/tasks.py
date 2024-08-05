from fastapi import BackgroundTasks, HTTPException, Request

from server.core.config import settings
from server.core.models.sql.accounts import Account
from server.core.schemas.utilities import MessageResponse
from server.utils.mail import send_mail
from server.utils.mail.links import get_account_activation_link


async def send_activation_mail(request: Request, account: Account) -> None:
    url = await get_account_activation_link(request, account)
    await send_mail(
        context={
            "request": request,
            "url": url,
            "username": account.username,
            "subject": f"Account activation for {account.first_name} {account.last_name}",
        },
        recipients=[account.email],
        template_name="account-activation.html",
    )


async def send_activation_successful_mail(request: Request, account: Account) -> None:
    await send_mail(
        context={
            "request": request,
            "username": account.username,
            "subject": "Account activation successful",
        },
        recipients=[account.email],
        template_name="account-activated.html",
    )


async def process_account_activation(
    request: Request,
    queue: BackgroundTasks,
    account: Account,
) -> MessageResponse:
    try:
        if settings.SEND_MAIL:
            queue.add_task(send_activation_mail, request, account)
            return MessageResponse(msg="Please check your mail to activate your account.")

        url = await get_account_activation_link(request, account)
        return MessageResponse(msg=f"Please visit {url} to activate your account")
    except HTTPException as e:
        raise e
