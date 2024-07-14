from pathlib import Path

import typer
from typer import Option, Typer

from cli.commands.utils.new_app import is_valid_service, make_new_app_files
from cli.commands.utils.new_endpoint import append_new_endpoint_contents

app = Typer()


@app.command(name="app")
def generate_new_app(
    name: str = Option(..., prompt="Name your app", help="Name of the new app"),
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


@app.command(name="endpoint")
def generate_endpoint(
    app: str = Option(
        ...,
        prompt="Name of the app where the endpoint will be created",
        help="Name of the app where the endpoint will be created",
    ),
    version: str = Option(
        "v1", prompt="Version of the app where the endpoint will be created", help="Version of the app where the endpoint will be created"
    ),
    endpoint: str = Option(
        "",
        prompt="Name of the new endpoint",
        help="Name of the new endpoint",
    ),
    method: str = Option(
        "GET",
        prompt="HTTP method for the endpoint",
        help="HTTP method for the endpoint",
    ),
    summary: str = Option(
        "",
        prompt="Summary of the endpoint",
        help="Summary of the endpoint",
    ),
    response_description: str = Option(
        "",
        prompt="Response description of the endpoint",
        help="Response description of the endpoint",
    ),
    handler: str = Option(
        ...,
        prompt="Name of the endpoint handler function",
        help="Name of the endpoint handler function",
    ),
):
    if is_valid_service(app):
        typer.echo(f"{app} app does not exist. Please create the app first.")
        return

    if endpoint:
        if endpoint == "/":
            endpoint = ""
        else:
            endpoint = f"/{endpoint}" if not endpoint.startswith("/") else endpoint

    append_new_endpoint_contents(app, version, endpoint, method, summary, response_description, handler)
