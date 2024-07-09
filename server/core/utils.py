from pathlib import Path


def validate_file(path: Path, extensions: list[str]) -> bool:
    # Check if the file has a .json extension
    if path.suffix.lower() not in [f".{e.lower()}" for e in extensions]:
        raise ValueError(f"Source file must be a {', '.join(extensions)} file")

    # Check if the file exists
    if not path.is_file():
        raise ValueError(f"File does not exist: {path}")

    return path
