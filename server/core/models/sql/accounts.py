from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.core.enums import Genders, Providers
from server.core.models.sql import Base


class Account(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    username: Mapped[str] = mapped_column(String(length=64), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(length=256), nullable=False, unique=True, index=True)
    open_id: Mapped[str] = mapped_column(String(length=256), nullable=True, index=True)
    _provider: Mapped[str] = mapped_column(String(length=16), nullable=True, index=True)
    _hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    _hash_salt: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    first_name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(length=256), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    _birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    _gender: Mapped[str] = mapped_column(String(length=1), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (UniqueConstraint("open_id", "_provider", name="uq_account_open_id_provider"),)

    groups: Mapped[list["Group"]] = relationship(
        "Group",
        secondary="group_accounts",
        back_populates="accounts",
        order_by="Group.name",
    )
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_accounts",
        back_populates="accounts",
        order_by="Role.name",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary="permission_accounts",
        back_populates="accounts",
        order_by="Permission.object_name, Permission.action",
    )

    @property
    def provider(self) -> Providers:
        if self._provider == Providers.GOOGLE:
            return Providers.GOOGLE
        elif self._provider == Providers.GITHUB:
            return Providers.GITHUB
        return None

    def set_provider(self, provider: Providers) -> None:
        self._provider = provider.value

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    def set_hashed_password(self, hashed_password: str) -> None:
        self._hashed_password = hashed_password

    @property
    def hash_salt(self) -> str:
        return self._hash_salt

    def set_hash_salt(self, hash_salt: str) -> None:
        self._hash_salt = hash_salt

    @property
    def gender(self) -> Genders:
        if self._gender == Genders.MALE:
            return Genders.MALE
        elif self._gender == Genders.FEMALE:
            return Genders.FEMALE

    def set_gender(self, gender: Genders) -> None:
        self._gender = gender.value

    @property
    def birth_date(self) -> date:
        return self._birth_date

    def set_birth_date(self, birth_date: date) -> None:
        self._birth_date = birth_date


class Group(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(length=64), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(length=256), nullable=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="group_roles",
        back_populates="groups",
        order_by="Role.name",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="group_accounts",
        back_populates="groups",
        order_by="Account.id",
    )


class Role(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(length=64), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(length=256), nullable=True)

    groups: Mapped[list["Group"]] = relationship(
        "Group",
        secondary="group_roles",
        back_populates="roles",
        order_by="Group.name",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
        order_by="Permission.object_name, Permission.action",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="role_accounts",
        back_populates="roles",
        order_by="Account.id",
    )


class Permission(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    object_name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    action: Mapped[str] = mapped_column(String(length=64), nullable=False)
    description: Mapped[str] = mapped_column(String(length=256), nullable=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions",
        order_by="Role.name",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="permission_accounts",
        back_populates="permissions",
        order_by="Account.id",
    )

    __table_args__ = (UniqueConstraint("object_name", "action", name="uq_permission_object_name_action"),)


class GroupRole(Base):
    group_id: Mapped[int] = mapped_column(
        ForeignKey(column="groups.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey(column="roles.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )


class RolePermission(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey(column="roles.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey(column="permissions.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )


class GroupAccount(Base):
    group_id: Mapped[int] = mapped_column(
        ForeignKey(column="groups.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey(column="accounts.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )


class RoleAccount(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey(column="roles.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey(column="accounts.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )


class PermissionAccount(Base):
    permission_id: Mapped[int] = mapped_column(
        ForeignKey(column="permissions.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey(column="accounts.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
