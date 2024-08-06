import pymongo
from beanie import Granularity, TimeSeriesConfig
from pydantic import Field, field_validator
from pymongo import IndexModel

from server.core.models.mongodb import BaseDocument
from server.core.schemas import BaseSchema
from server.core.schemas.utilities import MetadataField


class RequestLog(BaseDocument):
    account_id: int | None = Field(None, description="Account ID of the user who made the request")
    endpoint: str = Field(..., description="API endpoint relative to the base URL")
    method: str = Field(..., description="HTTP method used for the request")
    query_params: dict | None = Field(None, description="Optional query parameters of the request")
    request_body: dict | None = Field(None, description="Optional request body of the request")
    headers: dict | None = Field(None, description="Optional request headers of the request")
    status_code: int | None = Field(None, description="Status code of the response")
    client_ip: str | None = Field(None, description="Client IP address from which the request was made")
    error_response: dict | None = Field(None, description="Error response in case of an error")
    metadata: MetadataField = Field(default_factory=dict)

    class Settings:
        indexes = [
            IndexModel([("account_id", pymongo.ASCENDING)]),
            IndexModel([("endpoint", pymongo.ASCENDING), ("method", pymongo.ASCENDING)]),
            IndexModel([("client_ip", pymongo.ASCENDING)]),
            IndexModel([("status_code", pymongo.ASCENDING)]),
        ]


class ChangeLog(BaseDocument):
    account_id: int | None = Field(None, description="Account ID of the user who made the change")
    resource_name: str = Field(..., description="Name of the resource that was changed")
    object_name: str = Field(..., description="Name of the object that was changed")
    object_id: int = Field(..., description="ID of the object that was changed")
    action: str = Field(..., description="Action that was performed on the object")
    old_value: dict | None = Field(None, description="Old value of the object")
    new_value: dict | None = Field(None, description="New value of the object")
    version_id: int = Field(1, description="Version ID of the object")

    class Settings:
        indexes = [
            IndexModel([("account_id", pymongo.ASCENDING)]),
            IndexModel([("resource_name", pymongo.ASCENDING), ("object_name", pymongo.ASCENDING)]),
            IndexModel([("object_id", pymongo.ASCENDING)]),
            IndexModel([("action", pymongo.ASCENDING)]),
        ]
        timeseries = TimeSeriesConfig(
            time_field="created_at",
            granularity=Granularity.seconds,
        )

    @field_validator("old_value", "new_value", mode="before")
    @classmethod
    def serialize_pydantic_model(cls, v: BaseSchema | dict) -> dict:
        if isinstance(v, BaseSchema):
            return v.model_dump()
        return v
