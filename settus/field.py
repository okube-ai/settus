from pydantic import Field as _Field
from pydantic.fields import FieldInfo as _FieldInfo

from azure.core.credentials import TokenCredential


class FieldInfo(_FieldInfo):
    kayvault_url: str | None = None
    kayvault_credentials: TokenCredential | None = None
    # TODO: Fix and use


def Field(
    *args,
    keyvault_url: str = None,
    keyvault_credentials: TokenCredential = None,
    **kwargs,
):
    field_info = _Field(
        *args,
        keyvault_url=keyvault_url,
        keyvault_credentials=keyvault_credentials,
        **kwargs,
    )
    # TODO: Create instance of FieldInfo instead of _FieldInfo
    return field_info
