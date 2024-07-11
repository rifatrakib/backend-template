from typing import Any

from server.core.schemas import BaseSchema


class HistoryDataSchema(BaseSchema):
    old_data: dict[str, Any] | None = None
    new_data: dict[str, Any] | None = None
