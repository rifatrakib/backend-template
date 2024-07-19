from fastapi import Request

from server.core.models.sql.accounts import Account
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
        template_name="activation.html",
    )
