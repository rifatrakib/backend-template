from datetime import date, datetime

from pydantic import EmailStr, Field

from server.core.enums import Genders
from server.core.schemas import BaseSchema


class PermissionSchema(BaseSchema):
    permission_id: int = Field(description="Permission ID", ge=1)
    object_name: str = Field(description="Name of the object this permission is for", max_length=64)
    action: str = Field(description="Action permitted on the object by this permission", max_length=64)
    description: str | None = Field(
        default=None,
        description="Optional explanation for this permission",
        max_length=256,
    )


class RoleSchema(BaseSchema):
    role_id: int = Field(description="Role ID", ge=1)
    name: str = Field(description="Name of the role", max_length=64)
    description: str | None = Field(
        default=None,
        description="Optional explanation for this role",
        max_length=256,
    )
    permissions: list[PermissionSchema] = Field(
        default_factory=list,
        description="List of permissions granted by this role",
    )


class GroupSchema(BaseSchema):
    group_id: int = Field(description="Group ID", ge=1)
    name: str = Field(description="Name of the group", max_length=64)
    description: str | None = Field(
        default=None,
        description="Optional explanation for this group",
        max_length=256,
    )
    roles: list[RoleSchema] = Field(default_factory=list, description="List of roles assigned to this group")


class AccountSchema(BaseSchema):
    account_id: int = Field(description="Account ID", ge=1)
    username: str = Field(description="Username", max_length=64)
    email: EmailStr = Field(description="Email address")
    open_id: str | None = Field(default=None, description="OpenID", max_length=256)
    provider: str | None = Field(default=None, description="Provider", max_length=16)
    first_name: str = Field(description="First name", max_length=64)
    middle_name: str | None = Field(default=None, description="Middle name", max_length=256)
    last_name: str = Field(description="Last name", max_length=64)
    birth_date: date | None = Field(default=None, description="Birth date")
    gender: Genders | None = Field(default=None, description="Gender (m/f)")
    is_verified: bool = Field(description="Is account verified")
    is_active: bool = Field(description="Is account active")
    is_superuser: bool = Field(description="Is account superuser")
    created_at: datetime = Field(description="Account creation timestamp")
    last_updated_at: datetime | None = Field(default=None, description="Last account update timestamp")
    delete_at: datetime | None = Field(default=None, description="Account deletion initiation timestamp")
    groups: list[GroupSchema] = Field(default_factory=list, description="List of groups this account belongs to")
    roles: list[RoleSchema] = Field(default_factory=list, description="List of roles assigned to this account")
    permissions: list[PermissionSchema] = Field(
        default_factory=list,
        description="List of permissions granted to this account",
    )
