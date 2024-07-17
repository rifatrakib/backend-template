import asyncio

from typer import Option, Typer

from cli.commands.utils.superuser import create_admin_superuser

app = Typer()


@app.command(name="superuser")
def create_superuser(
    username: str = Option(..., prompt=True),
    email: str = Option(..., prompt=True),
    password: str = Option(..., prompt=True, confirmation_prompt=True, hide_input=True),
    first_name: str = Option(..., prompt=True),
    last_name: str = Option(..., prompt=True),
):
    """Create a superuser."""
    print(f"Creating superuser {username} with email {email}")
    asyncio.run(create_admin_superuser(username, email, password, first_name, last_name))
