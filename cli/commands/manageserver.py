import typer
import uvicorn

app = typer.Typer()


@app.command(name="start")
def start_server():
    uvicorn.run(
        "server.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
