from pathlib import Path

import typer
from typer import Option, Typer

from cli.commands.utils.new_app import is_valid_service, make_new_app_files

app = Typer()


@app.command(name="app")
def generate_new_app(
    name: str = Option(..., prompt=True, help="Name of the new app"),
):
    if not is_valid_service(name):
        typer.echo(f"{name} app already exists. This command will overwrite the existing app and may not be reversible.")
        if not typer.confirm("Are you sure you want to overwrite the existing app?"):
            typer.echo("App not created. Exiting...")
            return

    # Create the app directory
    directory = Path(f"server/routes/{name}")
    directory.mkdir(parents=True, exist_ok=True)

    # Create the __init__.py file in server/routes if it doesn't exist
    init_file = Path("server/routes/__init__.py")
    if not init_file.exists():
        init_file.touch()

    # Create the docs directory for the first version of the app routes
    docs_directory = Path(f"{directory}/docs/v1")
    docs_directory.mkdir(parents=True, exist_ok=True)

    # Create and write the files for the new app
    make_new_app_files(name, directory)
