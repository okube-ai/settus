from __future__ import annotations as _annotations

from pathlib import Path
from collections import defaultdict
from typing import Any
from typing import Tuple
from typing import Type
from pydantic import ConfigDict
from pydantic import AliasChoices
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

from settus.settingssources.azurekeyvault import AzureKeyVault
from settus.settingssources.awssecretsmanager import AWSSecretsManager


class BaseSettings(_BaseSettings):
    """
    Base Settings class.

    Examples
    --------
    ```py
    import os
    from settus import BaseSettings
    from settus import Field
    from settus import SettingsConfigDict

    KEYVAULT_URL = "https://o3-kv-settus-dev.vault.azure.net/"
    os.environ["MY_ENV"] = "my_value"

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(keyvault_url=KEYVAULT_URL)
        my_env: str = Field(default="undefined")
        my_azure_secret: str = Field(default="undefined", alias="my-secret")

    settings = Settings()
    print(settings)
    #> my_env='my_value' my_azure_secret='secretsauce'
    ```
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    @property
    def model_field_alias(self) -> list:
        aliases = []
        for k, f in self.model_fields.items():
            alias = f.alias
            if isinstance(alias, str):
                aliases += [(k, alias)]
            elif isinstance(alias, AliasChoices):
                for a in alias.choices:
                    aliases += [(k, a)]
        return aliases

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[_BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """
        Supported sources and priority. Can be subclassed to overwrite the
        default priority list:

        * Init values
        * Environment variables
        * Azure keyvault settings
        * AWS Secrets Manager

        Parameters
        ----------
        settings_cls:
            Definition of base class
        init_settings:
            Values provided from fields init
        env_settings:
            Values provided from environment variables
        dotenv_settings:
            Values provided from .env file
        file_secret_settings:
            Values provided from secrets file
        """
        # Highest priority listed first
        return (
            init_settings,
            env_settings,
            AzureKeyVault(settings_cls),
            AWSSecretsManager(settings_cls),
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
        # ------------------------------------------------------------------- #
        # Settus-specific validation                                          #
        # ------------------------------------------------------------------- #

        # Config
        if not self.model_config["populate_by_name"]:
            raise ValueError(
                "Model configuration `populate_by_name` must be set to False"
                " when using settus.BaseSettings"
            )

        # Initialization values
        for k in init_kwargs:
            for f, a in self.model_field_alias:
                if k == a:
                    raise AttributeError(
                        f"Attribute {a} is an alias and should not be set in the class"
                        f"initialization. Instead set {f} to avoid conflicts."
                    )

        # ------------------------------------------------------------------- #
        # END-OF-VALIDATION                                                   #
        # ------------------------------------------------------------------- #

        # Determine settings config values
        case_sensitive = (
            _case_sensitive
            if _case_sensitive is not None
            else self.model_config.get("case_sensitive")
        )
        env_prefix = (
            _env_prefix
            if _env_prefix is not None
            else self.model_config.get("env_prefix")
        )
        env_file = (
            _env_file
            if _env_file != ENV_FILE_SENTINEL
            else self.model_config.get("env_file")
        )
        env_file_encoding = (
            _env_file_encoding
            if _env_file_encoding is not None
            else self.model_config.get("env_file_encoding")
        )
        env_nested_delimiter = (
            _env_nested_delimiter
            if _env_nested_delimiter is not None
            else self.model_config.get("env_nested_delimiter")
        )
        secrets_dir = (
            _secrets_dir
            if _secrets_dir is not None
            else self.model_config.get("secrets_dir")
        )

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
            self.__class__,
            secrets_dir=secrets_dir,
            case_sensitive=case_sensitive,
            env_prefix=env_prefix,
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
            # --------------------------------------------------------------- #
            # Settus-specific parsing                                         #
            # --------------------------------------------------------------- #

            # This section is re-written from base class to map all alias to
            # field names. This helps prevent issues when a value is found for
            # both the field name and the alias(es). A common scenario is when
            # a value is found for both an environment variable matching the
            # alias and an init value matching the field name.

            # Build map
            _map = defaultdict(lambda: [])
            for k, f in self.model_fields.items():
                alias = f.alias
                if isinstance(alias, str):
                    _map[alias] += [k]
                elif isinstance(alias, AliasChoices):
                    for a in alias.choices:
                        _map[a] += [k]

            _sources = []
            for d in [s() for s in sources]:
                for k, v in list(d.items()):
                    if k in _map:
                        for _v in _map[k]:
                            d[_v] = v
                            if _v not in d:
                                d[_v] = v
                        del d[k]
                _sources += [d]

            return deep_update(*reversed(_sources))

        else:
            # no one should mean to do this, but I think returning an empty dict is marginally preferable
            # to an informative error and much better than a confusing error
            return {}
