# Settus

Settings management using Pydantic Settings and extended to secrets from Azure Keyvault, Databricks secrets [IN PROGRESS], AWS Secrets Manager [IN PROGRESS] and GCP Secrets Manager [IN PROGRESS]

## Okube Company

Okube is committed to develop open source data engineering and ML engineering tools. Contributions are more than welcome.


## Installation

Install using `pip install -U settus[{cloud_provider}]` where `{cloud_provider}` is the cloud provider(s) you want to fetch secrets from. Possible options are:
- azure
- aws
- gcp
- databricks

## Getting started

Settus uses [Pydantic Settings management](https://docs.pydantic.dev/latest/usage/pydantic_settings/) as its foundation. In addition, it defines the settings sources mentioned below to fetch secrets from cloud providers. The default priority order is as follows:
- Init Settings
- Environment variables 
- Azure KeyVault
- AWS Secrets Manager
- GCP Secrets Manager
- Databricks secrets

In other words, if a setting is not available from the initialization or from an environment variable, it wil sequentially lookup the field name (or aliases) in the other available sources. 

### Azure Key Vault
By providing the `keyvault_url` to the `SettingsConfigDict` or to a given field. The keyvault credentials can also be provided. Otherwise, the [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python) is used. Similarly to environment variables, aliases may be used to set the key of the secrets.

### AWS Secrets Manager
TODO

### GCP Secrets Manager
TODO

### Databricks Secrets
TODO

## A Simple Example

```py
import os
from settus import BaseSettings
from settus import Field
from settus import SettingsConfigDict

KEYVAULT_URL = "https://my-keyvault.vault.azure.net/"

os.environ["MY_ENV"] = "my_value"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(keyvault_url="https://my-keyvault.vault.azure.net/")
    my_env: str = Field(default="undefined")  # value from ENV VAR
    my_secret: str = Field(default="undefined", alias="my-secret")  # value from KeyVault

settings = ()
print(settings.my_env)
#> my_value
print(settings.my_secret)
#> secret_sauce
```

## Contributing

TODO

## Reporting a Security Vulnerability

TODO
