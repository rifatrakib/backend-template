from pydantic import EmailStr, Field, HttpUrl

from server.core.schemas import BaseSchema


class Contact(BaseSchema):
    name: str
    url: HttpUrl
    email: EmailStr


class APIConfig(BaseSchema):
    title: str
    description: str
    version: str
    terms_of_service: HttpUrl
    contact: Contact
    openapi_url: str
    docs_url: str
    redoc_url: str


class ExternalDocs(BaseSchema):
    description: str
    url: HttpUrl


class OpenAPITags(BaseSchema):
    name: str
    description: str
    external_docs: ExternalDocs = Field(
        alias="externalDocs",
        default_factory=dict,
    )


class OpenAPIConfig(APIConfig):
    tags_metadata: list[OpenAPITags] = Field(default_factory=list)
