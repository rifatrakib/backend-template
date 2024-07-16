from pathlib import Path


def endpoint_contents(handler: str, method: str, endpoint: str, summary: str, response_description: str) -> str:
    contents = f"""
    @router.{method.lower()}(
        "{endpoint}",
        summary="{summary}",
        response_description="{response_description}",
    )
    async def {handler}():
        try:
            return await controllers.{handler}()
        except HTTPException as e:
            raise e
"""

    return contents


def controller_contents(handler: str) -> str:
    contents = f"""

async def {handler}():
    pass
"""

    return contents


def endpoint_docs_content(name: str) -> str:
    with open("cli/commands/templates/new-endpoint.md") as f:
        contents = f.read()
    return contents


def append_new_endpoint_contents(
    name: str, version: str, endpoint: str, method: str, summary: str, response_description: str, handler: str
) -> None:
    # Create the endpoint handler function
    endpoint_file = Path(f"server/routes/{name}/{version}/__init__.py")
    with open(endpoint_file, "r") as reader:
        lines = reader.readlines()

    contents = endpoint_contents(handler, method, endpoint, summary, response_description)
    endpoint_file_contents = "".join(lines[:-2]) + contents + "".join(lines[-2:])
    endpoint_file.write_text(endpoint_file_contents)

    # Create the endpoint controller function
    endpoint_file = Path(f"server/routes/{name}/{version}/controllers.py")
    with open(endpoint_file, "a") as writer:
        writer.write(controller_contents(handler))

    # Create the endpoint documentation file
    endpoint_doc_file = Path(f"server/routes/{name}/{version}/docs/{handler}.md")
    endpoint_doc_file.write_text(endpoint_docs_content(name))
