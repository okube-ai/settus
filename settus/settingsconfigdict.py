from pydantic_settings import SettingsConfigDict as _SettingsConfigDict
from pydantic_settings.main import config_keys

from azure.core.credentials import TokenCredential


class SettingsConfigDict(_SettingsConfigDict, total=False):
    keyvault_url: str | None
    keyvault_credentials: TokenCredential | None


config_keys |= set(SettingsConfigDict.__annotations__.keys())
