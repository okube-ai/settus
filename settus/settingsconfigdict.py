from pydantic_settings import SettingsConfigDict as _SettingsConfigDict
from pydantic_settings.main import config_keys


class SettingsConfigDict(_SettingsConfigDict, total=False):
    keyvault_url: str | None


config_keys |= set(SettingsConfigDict.__annotations__.keys())
