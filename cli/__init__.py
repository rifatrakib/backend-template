import typer

from cli.commands import health, manageserver


def configure_cli() -> typer.Typer:
    app = typer.Typer()

    app.add_typer(health.app, name="health")
    app.add_typer(manageserver.app, name="server")

    return app
