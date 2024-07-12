from pymongo import IndexModel

from server.core.models.mongodb import BaseDocument
from server.core.schemas.accounts import AccountSchema


class AccountCache(BaseDocument, AccountSchema):
    class Settings:
        name = "accounts"
        indexes = [
            IndexModel("account_id", unique=True),
            IndexModel("username", unique=True),
            IndexModel("email", unique=True),
            IndexModel(["open_id", "provider"], unique=True),
        ]
