from typing import Union
from typing import Any
from pydantic import Field as _Field
from pydantic.fields import FieldInfo as _FieldInfo


C = Any
try:
    from azure.core.credentials import TokenCredential as C
except ModuleNotFoundError:
    pass


class FieldInfo(_FieldInfo):
    kayvault_url: Union[str, None] = None
    kayvault_credentials: Union[C, None] = None
    aws_secret_name: Union[str, None] = None
    # TODO: Fix and use


def Field(
    *args,
    keyvault_url: str = None,
    keyvault_credentials: C = None,
    **kwargs,
) -> _Field:
    """
    Settus Field

    Parameters
    ----------
    args:
        Pydantic field args
    keyvault_url:
        Keyvault URL for this specific field. Overwrite model config.
    keyvault_credentials
        Keyvault credentials for this specific field.  Overwrite model config.
    kwargs
        Pydantic field kwargs

    Returns
    -------
    :
        Field

    Examples
    --------
    ```py
    from settus import BaseSettings
    from settus import Field

    class Settings(BaseSettings):
        my_azure_secret: str = Field(
            default="undefined",
            alias="my-secret",
            keyvault_url="https://o3-kv-settus-dev.vault.azure.net/",
        )

    settings = Settings()
    print(settings)
    #> my_azure_secret='secretsauce'
    ```
    """
    field_info = _Field(
        *args,
        keyvault_url=keyvault_url,
        keyvault_credentials=keyvault_credentials,
        **kwargs,
    )
    # TODO: Create instance of FieldInfo instead of _FieldInfo
    return field_info
