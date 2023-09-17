from typing import Tuple
from typing import Type
from pydantic import ConfigDict
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import PydanticBaseSettingsSource

from .keyvaultsettingssource import KeyVaultSettingsSource


class BaseSettings(_BaseSettings):
    model_config = ConfigDict(populate_by_name=True)

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
