from server.core.schemas import BaseSchema


class MetadataField(BaseSchema):
    environment: str
    source: str
