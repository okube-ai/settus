Settus uses [Pydantic Settings management](https://docs.pydantic.dev/latest/usage/pydantic_settings/) as its foundation. 
In addition, it defines the settings sources mentioned below to fetch secrets from cloud providers.
The default priority order is as follows:

* Init Settings
* Environment variables 
* Azure KeyVault
* AWS Secrets Manager
* GCP Secrets Manager
* Databricks secrets

In other words, if a setting is not available from the initialization or from an environment variable, it wil sequentially lookup the field name (or aliases) in the other available sources. 

### Azure Key Vault
To use Azure Keyvault, log in using Azure CLI or set these environment variables:

* `AZURE_TENANT_ID`
* `AZURE_CLIENT_ID`
* `AZURE_CLIENT_SECRET`

More logging in options are described [here](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python).

In addition, provide `keyvault_url` either to `SettingsConfigDict` or to a given field.

### AWS Secrets Manager
To use AWS Secrets Manager, log in using AWS CLI or set these environment variables:

* `AWS_REGION`
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

More logging in options are described [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

In addition, provide `aws_secret_name` either to `SettingsConfigDict` or to a given field.


### GCP Secrets Manager
TODO

### Databricks Secrets
TODO

## A Simple Example

```py
import os
from settus import BaseSettings
from settus import Field

KEYVAULT_URL = "https://o3-kv-settus-dev.vault.azure.net/"
AWS_SECRET_NAME = "vault"

os.environ["MY_ENV"] = "my_value"


class Settings(BaseSettings):
    # Value from environment variable "MY_ENV"
    my_env: str = Field(default="undefined")

    # Value from the Azure keyvault named `o3-kv-settus-dev` with secret key `my-secret`
    my_azure_secret: str = Field(
        default="undefined", alias="my-secret", keyvault_url=KEYVAULT_URL
    )

    # Value from the secret named `vault` in AWS secrets manager and having the secret key `my-secret`
    my_aws_secret: str = Field(
        default="undefined", alias="my-secret", aws_secret_name=AWS_SECRET_NAME
    )


settings = Settings()
print(settings.my_env)
#> my_value
print(settings.my_azure_secret)
#> secretsauce
print(settings.my_aws_secret)
#> secretsauce
```

## Configuration Dict Example

When multiple settings share the same keyvault or aws secret, a global setting may be defined.
In this case, Azure Keyvault will be called (assuming proper credentials are available) and if
no value has been found, it will fall back on AWS Secrets. Changing the order of priorities is
possible as described [here](https://docs.pydantic.dev/latest/usage/pydantic_settings/#changing-priority).

```py
import os
from settus import BaseSettings
from settus import Field
from settus import SettingsConfigDict

KEYVAULT_URL = "https://o3-kv-settus-dev.vault.azure.net/"
AWS_SECRET_NAME = "vault"

os.environ["MY_ENV"] = "my_value"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        keyvault_url=KEYVAULT_URL, aws_secret_name=AWS_SECRET_NAME
    )
    my_env: str = Field(default="undefined")
    my_azure_secret: str = Field(default="undefined", alias="my-secret")
    my_aws_secret: str = Field(default="undefined", alias="my-secret")


settings = Settings()
print(settings.my_env)
#> my_value
print(settings.my_azure_secret)
#> secretsauce
print(settings.my_aws_secret)
#> secretsauce
```
