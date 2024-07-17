import typer

from cli.commands import create, generate, health, server


def configure_cli() -> typer.Typer:
    app = typer.Typer()

    app.add_typer(health.app, name="health")
    app.add_typer(generate.app, name="generate")
    app.add_typer(server.app, name="server")
    app.add_typer(create.app, name="create")

    return app
