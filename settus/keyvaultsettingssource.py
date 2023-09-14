from typing import Any, Dict, Tuple

from pydantic.fields import FieldInfo
from pydantic_settings.sources import PydanticBaseEnvSettingsSource

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError
from azure.core.exceptions import HttpResponseError


class KeyVaultSettingsSource(PydanticBaseEnvSettingsSource):
    """
    Azure Key Vault settings source class that loads variables from an azure
    secrets manager resource.
    """

    def get_field_value(
            self,
            field: FieldInfo,
            field_name: str
    ) -> Tuple[Any, str, bool]:

        # Check if URL exists
        keyvault_url = self.config.get("keyvault_url")

        if keyvault_url is None:
            return None, field_name, False

        client = SecretClient(
            vault_url=keyvault_url,
            credential=DefaultAzureCredential()
        )
        env_val: str | None = None
        for field_key, env_name, value_is_complex in self._extract_field_info(field, field_name):
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