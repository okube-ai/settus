from __future__ import annotations as _annotations

from pathlib import Path
from typing import Any
from typing import Tuple
from typing import Type
from pydantic import ConfigDict
from pydantic._internal._utils import deep_update
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings.sources import (
    ENV_FILE_SENTINEL,
    DotEnvSettingsSource,
    DotenvType,
    EnvSettingsSource,
    InitSettingsSource,
    SecretsSettingsSource,
)

from .keyvaultsettingssource import KeyVaultSettingsSource


class BaseSettings(_BaseSettings):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[_BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        # Highest priority listed first
        return (
            init_settings,
            env_settings,
            KeyVaultSettingsSource(settings_cls),
            # file_secret_settings,
        )

    def _settings_build_values(
        self,
        init_kwargs: dict[str, Any],
        _case_sensitive: bool | None = None,
        _env_prefix: str | None = None,
        _env_file: DotenvType | None = None,
        _env_file_encoding: str | None = None,
        _env_nested_delimiter: str | None = None,
        _secrets_dir: str | Path | None = None,
    ) -> dict[str, Any]:
        # Determine settings config values
        case_sensitive = _case_sensitive if _case_sensitive is not None else self.model_config.get('case_sensitive')
        env_prefix = _env_prefix if _env_prefix is not None else self.model_config.get('env_prefix')
        env_file = _env_file if _env_file != ENV_FILE_SENTINEL else self.model_config.get('env_file')
        env_file_encoding = (
            _env_file_encoding if _env_file_encoding is not None else self.model_config.get('env_file_encoding')
        )
        env_nested_delimiter = (
            _env_nested_delimiter
            if _env_nested_delimiter is not None
            else self.model_config.get('env_nested_delimiter')
        )
        secrets_dir = _secrets_dir if _secrets_dir is not None else self.model_config.get('secrets_dir')

        # Configure built-in sources
        init_settings = InitSettingsSource(self.__class__, init_kwargs=init_kwargs)
        env_settings = EnvSettingsSource(
            self.__class__,
            case_sensitive=case_sensitive,
            env_prefix=env_prefix,
            env_nested_delimiter=env_nested_delimiter,
        )
        dotenv_settings = DotEnvSettingsSource(
            self.__class__,
            env_file=env_file,
            env_file_encoding=env_file_encoding,
            case_sensitive=case_sensitive,
            env_prefix=env_prefix,
            env_nested_delimiter=env_nested_delimiter,
        )

        file_secret_settings = SecretsSettingsSource(
            self.__class__, secrets_dir=secrets_dir, case_sensitive=case_sensitive, env_prefix=env_prefix
        )
        # Provide a hook to set built-in sources priority and add / remove sources
        sources = self.settings_customise_sources(
            self.__class__,
            init_settings=init_settings,
            env_settings=env_settings,
            dotenv_settings=dotenv_settings,
            file_secret_settings=file_secret_settings,
        )
        if sources:
            # This section is re-written to map all alias to field names. This helps prevent issues when a value is
            # found for both the field name and the alias(es). A common scenario is when a value is found for both
            # an environment variable matching the alias and an init value matching the field name.

            # Build map
            # TODO: Add support when populate_by_name is False and when multiple aliases are provided.
            _map = {}
            for k, f in self.model_fields.items():
                alias = f.alias
                if alias is not None:
                    _map[alias] = k

            _sources = []
            for d in [s() for s in sources]:
                for k, v in list(d.items()):
                    if k in _map:
                        d[_map[k]] = v
                        del d[k]
                _sources += [d]

            return deep_update(*reversed(_sources))
            # return deep_update(*reversed([source() for source in sources]))
        else:
            # no one should mean to do this, but I think returning an empty dict is marginally preferable
            # to an informative error and much better than a confusing error
            return {}
