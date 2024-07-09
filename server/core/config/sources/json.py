import json
import os
from pathlib import Path
from typing import Any, Type

from pydantic import field_validator
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from server.core.schemas import BaseConfig
from server.core.utils import validate_file


class SettingsSource(PydanticBaseSettingsSource):
    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        pass

    def read_secrets(self) -> dict[str, Any]:
        with open(os.getenv("SOURCE")) as file:
            return json.load(file)

    def __call__(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
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
        validate_file(path, ["json"])

        # Attempt to open and parse the JSON file to validate its content
        try:
            with path.open("r") as reader:
                json.load(reader)
        except (json.JSONDecodeError, OSError) as e:
            raise ValueError(f"Invalid JSON file: {e}")

        return value
