import os
from pathlib import Path
from typing import Any, Dict, Type

import yaml
from pydantic import field_validator
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from server.core.schemas import BaseConfig
from server.core.utils import validate_file


class SettingsSource(PydanticBaseSettingsSource):
    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        pass

    def read_secrets(self) -> Dict[str, Any]:
        with open(os.getenv("SOURCE")) as file:
            return yaml.safe_load(file)

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        secrets = self.read_secrets()

        for name in self.settings_cls.model_fields.keys():
            value = secrets.get(name)
            if value is not None:
                d[name] = value

        return d


class ConfigSource(BaseConfig):
    SOURCE: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, dotenv_settings, file_secret_settings, SettingsSource(settings_cls)

    @field_validator("SOURCE", mode="before")
    @classmethod
    def validate_source(cls, value: str) -> str:
        path = Path(value)
        validate_file(path, ["yaml", "yml"])

        # Attempt to open and parse the YAML file to validate its content
        try:
            with path.open("r") as file:
                yaml.safe_load(file)
        except (yaml.YAMLError, OSError) as e:
            raise ValueError(f"Invalid YAML file: {e}")

        return value
