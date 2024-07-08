from cli import configure_cli


def start_cli():
    app = configure_cli()
    return app()


if __name__ == "__main__":
    start_cli()
