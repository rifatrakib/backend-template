from sqlalchemy.ext.asyncio import AsyncSession

from server.core.connections import get_database_session
from server.core.models.sql.accounts import Account, Group, Permission, Role
from server.utils.managers import password_manager


def create_admin_permissions() -> list[Permission]:
    permissions = [
        Permission(object_name="*", action="create", description="Create any object"),
        Permission(object_name="*", action="read", description="Read any object"),
        Permission(object_name="*", action="update", description="Update any object"),
        Permission(object_name="*", action="delete", description="Delete any object"),
    ]
    return permissions


def create_admin_role() -> Role:
    role = Role(name="admin", description="Administrator role")
    role.permissions = create_admin_permissions()
    return role


def create_admin_group() -> Group:
    group = Group(name="admin", description="Administrator group")
    group.roles = [create_admin_role()]
    return group


async def create_admin_superuser(
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
) -> None:
    session: AsyncSession = get_database_session()
    # Create the superuser
    admin_account = Account(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=True,
        is_verified=True,
        is_superuser=True,
    )

    admin_account.groups = [create_admin_group()]
    hash_salt = password_manager.generate_hash_salt()
    admin_account.set_hash_salt(hash_salt)
    admin_account.set_hashed_password(
        password_manager.generate_hashed_password(hash_salt, password),
    )

    try:
        session.add(admin_account)
        await session.commit()
        await session.close()
        print(f"Superuser {username} created successfully.")
    except Exception as e:
        print(f"Error creating superuser: {e}")
        await session.rollback()
        await session.close()
        raise e
