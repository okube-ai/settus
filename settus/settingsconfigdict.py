from typing import Union
from pydantic_settings import SettingsConfigDict as _SettingsConfigDict
from pydantic_settings.main import config_keys

from azure.core.credentials import TokenCredential


class SettingsConfigDict(_SettingsConfigDict, total=False):
    keyvault_url: Union[str, None]
    keyvault_credentials: Union[TokenCredential, None]
    aws_secret_name: Union[str, None]


config_keys |= set(SettingsConfigDict.__annotations__.keys())
