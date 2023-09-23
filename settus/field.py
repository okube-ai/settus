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
):
    field_info = _Field(
        *args,
        keyvault_url=keyvault_url,
        keyvault_credentials=keyvault_credentials,
        **kwargs,
    )
    # TODO: Create instance of FieldInfo instead of _FieldInfo
    return field_info
