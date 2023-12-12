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
    """
    Cloud configuration

    Attributes
    ----------
    keyvault_url:
        Keyvault URL
    keyvault_credentials:
        Azure Token credentials
    aws_secret_name:
        AWS secret name

    Examples
    --------
    ```py
    from settus import BaseSettings
    from settus import Field
    from settus import SettingsConfigDict

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            keyvault_url="https://o3-kv-settus-dev.vault.azure.net/"
        )
        my_azure_secret: str = Field(default="undefined", alias="my-secret")

    settings = Settings()
    print(settings)
    #> my_azure_secret='secretsauce'
    ```
    """

    keyvault_url: Union[str, None]
    keyvault_credentials: Union[C, None]
    aws_secret_name: Union[str, None]


config_keys |= set(SettingsConfigDict.__annotations__.keys())
