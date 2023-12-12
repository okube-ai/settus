from typing import Any, Dict, Tuple, Union

from pydantic.fields import FieldInfo
from pydantic_settings.sources import PydanticBaseEnvSettingsSource


class AzureKeyVault(PydanticBaseEnvSettingsSource):
    """
    Azure Key Vault settings source class that loads variables from an azure
    secrets manager resource.
    """

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        """
        Get field value from keyvault

        Parameters
        ----------
        field:
            Field
        field_name
            Field name

        Returns
        -------
        field_value, field_key, is_complex
            Output used in `__call__` method
        """
        keyvault_url = None
        keyvault_credentials = None

        # Get keyvault from field
        if field.json_schema_extra is not None:
            keyvault_url = field.json_schema_extra.get("keyvault_url")
            keyvault_credentials = field.json_schema_extra.get("keyvault_credentials")

        # Get keyvault from config
        if keyvault_url is None:
            keyvault_url = self.config.get("keyvault_url")

        if keyvault_url is None:
            return None, field_name, False

        if keyvault_credentials is None:
            keyvault_credentials = self.config.get("keyvault_credentials")

        # Default credentials
        # https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview#sequence-of-authentication-methods-when-you-use-defaultazurecredential
        # The most common approach here is to set the following environment variables:
        #  - AZURE_TENANT_ID
        #  - AZURE_CLIENT_ID
        #  - AZURE_CLIENT_SECRET
        from azure.core.exceptions import ResourceNotFoundError
        from azure.core.exceptions import HttpResponseError
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        if keyvault_credentials is None:
            keyvault_credentials = DefaultAzureCredential()

        # Keyvault client
        client = SecretClient(vault_url=keyvault_url, credential=keyvault_credentials)
        env_val: Union[str, None] = None
        for field_key, env_name, value_is_complex in self._extract_field_info(
            field, field_name
        ):
            if "_" in env_name:
                continue
            try:
                env_val = client.get_secret(env_name).value
            except (ResourceNotFoundError, HttpResponseError):
                env_val = None
            if env_val is not None:
                break

        return env_val, field_key, value_is_complex

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d
