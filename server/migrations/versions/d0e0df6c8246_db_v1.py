"""db_v1.

Revision ID: d0e0df6c8246
Revises:
Create Date: 2024-07-11 17:11:49.589484
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

from server.core.models.sql import PydanticJSONType
from server.core.models.sql.schemas import HistoryDataSchema

# revision identifiers, used by Alembic.
revision: str = "d0e0df6c8246"  # pragma: allowlist secret
down_revision: str | None = None  # pragma: allowlist secret
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("email", sa.String(length=256), nullable=True),
        sa.Column("open_id", sa.String(length=256), nullable=True),
        sa.Column("_provider", sa.String(length=16), nullable=True),
        sa.Column("_hashed_password", sa.String(length=1024), nullable=True),
        sa.Column("_hash_salt", sa.String(length=1024), nullable=True),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("middle_name", sa.String(length=256), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("_birth_date", sa.Date(), nullable=True),
        sa.Column("_gender", sa.String(length=1), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("open_id", "_provider", name="uq_account_open_id_provider"),
    )
    op.create_index(op.f("ix_accounts__provider"), "accounts", ["_provider"], unique=False)
    op.create_index(op.f("ix_accounts_email"), "accounts", ["email"], unique=True)
    op.create_index(op.f("ix_accounts_open_id"), "accounts", ["open_id"], unique=False)
    op.create_index(op.f("ix_accounts_username"), "accounts", ["username"], unique=True)
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_groups_name"), "groups", ["name"], unique=True)
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("object_name", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("object_name", "action", name="uq_permission_object_name_action"),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_roles_name"), "roles", ["name"], unique=True)
    op.create_table(
        "group_accounts",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("group_id", "account_id"),
    )
    op.create_table(
        "group_roles",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("group_id", "role_id"),
    )
    op.create_table(
        "histories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("table_name", sa.String(length=64), nullable=False),
        sa.Column("row_id", sa.Integer(), nullable=False),
        sa.Column("operation", sa.String(length=16), nullable=False),
        sa.Column("data", PydanticJSONType(HistoryDataSchema), nullable=False),
        sa.Column("initiator_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_histories_account_id"), "histories", ["account_id"], unique=False)
    op.create_table(
        "permission_accounts",
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("permission_id", "account_id"),
    )
    op.create_table(
        "role_accounts",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "account_id"),
    )
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delete_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("role_permissions")
    op.drop_table("role_accounts")
    op.drop_table("permission_accounts")
    op.drop_index(op.f("ix_histories_account_id"), table_name="histories")
    op.drop_table("histories")
    op.drop_table("group_roles")
    op.drop_table("group_accounts")
    op.drop_index(op.f("ix_roles_name"), table_name="roles")
    op.drop_table("roles")
    op.drop_table("permissions")
    op.drop_index(op.f("ix_groups_name"), table_name="groups")
    op.drop_table("groups")
    op.drop_index(op.f("ix_accounts_username"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_open_id"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_email"), table_name="accounts")
    op.drop_index(op.f("ix_accounts__provider"), table_name="accounts")
    op.drop_table("accounts")
    # ### end Alembic commands ###
