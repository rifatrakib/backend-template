import subprocess

import typer

app = typer.Typer()


@app.command(name="start")
def start_server():
    subprocess.run("docker-compose up --build", shell=True)


@app.command(name="stop")
def stop_server():
    subprocess.run("docker-compose down", shell=True)
    subprocess.run('docker image prune --force --filter "dangling=true"', shell=True)
