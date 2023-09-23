from typing import Union
from typing import Any
from pydantic_settings import SettingsConfigDict as _SettingsConfigDict
from pydantic_settings.main import config_keys

C = Any
try:
    from azure.core.credentials import TokenCredential as C
except ModuleNotFoundError:
    pass


class SettingsConfigDict(_SettingsConfigDict, total=False):
    keyvault_url: Union[str, None]
    keyvault_credentials: Union[C, None]
    aws_secret_name: Union[str, None]


config_keys |= set(SettingsConfigDict.__annotations__.keys())
