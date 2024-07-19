import subprocess

from typer import Option, Typer

from server.core.config import settings

app = Typer()


@app.command(name="start")
def start_server(build: bool = Option(True)):
    if settings.TEST_RUN:
        subprocess.run("uvicorn server.main:app --reload", shell=True)

    command = "docker compose up --build" if build else "docker compose up"
    subprocess.run(command, shell=True)


@app.command(name="stop")
def stop_server():
    subprocess.run("docker-compose down", shell=True)
    subprocess.run('docker image prune --force --filter "dangling=true"', shell=True)
