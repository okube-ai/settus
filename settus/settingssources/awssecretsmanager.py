import os
import json
from typing import Any, Dict, Tuple, Union

from pydantic.fields import FieldInfo
from pydantic_settings.sources import PydanticBaseEnvSettingsSource


class AWSSecretsManager(PydanticBaseEnvSettingsSource):
    """
    AWS Secrets settings source class that loads variables from an AWS
    secrets manager resource.
    """

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        """
        Get field value from AWS Secrets Manager

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
        secret_name = None

        # Get keyvault from field
        if field.json_schema_extra is not None:
            secret_name = field.json_schema_extra.get("aws_secret_name")

        # Get keyvault from config
        if secret_name is None:
            secret_name = self.config.get("aws_secret_name")

        if secret_name is None:
            return None, field_name, False

        # Default credentials
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
        # The most common approach here is to set the following environment variables:
        #  - AWS_ACCESS_KEY_ID
        #  - AWS_SECRET_ACCESS_KEY
        #  - AWS_REGION
        import boto3
        from botocore.exceptions import ClientError

        # Session
        session = boto3.session.Session()

        # Client
        client = session.client(
            service_name="secretsmanager", region_name=os.getenv("AWS_REGION")
        )

        env_val: Union[str, None] = None
        for field_key, env_name, value_is_complex in self._extract_field_info(
            field, field_name
        ):
            try:
                var = client.get_secret_value(SecretId=secret_name)["SecretString"]
                try:
                    var = json.loads(var)
                    try:
                        env_val = var[env_name]
                    except KeyError as e:
                        pass
                except TypeError as e:
                    raise TypeError("Secret variable should by type key/value pair")
            except ClientError as e:
                pass
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
