import typer

app = typer.Typer()


@app.command(name="check")
def check():
    typer.echo("CLI is working fine!")
