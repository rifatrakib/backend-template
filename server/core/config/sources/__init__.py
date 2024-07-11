import os
from typing import Type

from server.core.config.sources import dotenv, json, yaml
from server.core.enums import EnvSources


def configure_env_source() -> list[Type]:
    source = os.environ.get("SOURCE", EnvSources.DOTENV)

    if source == EnvSources.JSON:
        return json.ConfigSource
    if source == EnvSources.YAML:
        return yaml.ConfigSource
    if source == EnvSources.DOTENV:
        return dotenv.ConfigSource


class ConfigSource(configure_env_source()):
    pass
