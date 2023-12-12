# Settus

[![pypi](https://img.shields.io/pypi/v/laktory.svg)](https://pypi.org/project/settus/)
[![test](https://github.com/okube-ai/settus/actions/workflows/test.yml/badge.svg)](https://github.com/okube-ai/settus/actions/workflows/test.yml)
[![downloads](https://static.pepy.tech/badge/settus/month)](https://pepy.tech/project/settus)
[![versions](https://img.shields.io/pypi/pyversions/settus.svg)](https://github.com/okube-ai/settus)
[![license](https://img.shields.io/github/license/okube-ai/settus.svg)](https://github.com/okube-ai/settus/blob/main/LICENSE)

Settings management using Pydantic Settings with cloud extensions.

Settus makes it possible to securely access local and cloud-stored secrets from multiple environments, with pre-defined fallback plans. Supported secrets provider are

* Azure Keyvault
* Databricks secrets [IN PROGRESS]
* AWS Secrets Manager
* GCP Secrets Manager [IN PROGRESS]

## Help
See [documentation](https://www.okube.ai/settus) for more details.


## Installation
Install using 
```commandline
pip install laktory[{cloud_provider}]
```
where `{cloud_provider}` is `azure`, `aws`, `databricks` or `gcp`. 

For more installation options,
see the [Install](https://www.okube.ai/settus/install/) section in the documentation.

## A Basic Example

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
    my_azure_secret: str = Field(default="undefined", alias="my-secret", keyvault_url=KEYVAULT_URL)
    
    # Value from the secret named `vault` in AWS secrets manager and having the secret key `my-secret`
    my_aws_secret: str = Field(default="undefined", alias="my-secret", aws_secret_name=AWS_SECRET_NAME)

settings = Settings()
print(settings.my_env)
#> my_value
print(settings.my_azure_secret)
#> secret_sauce
print(settings.my_aws_secret)
#> secret_sauce
```

To get started with more examples, jump into the [Quickstart](https://www.okube.ai/settus/quickstart/).

## Okube Company
Okube is dedicated to build open source frameworks, the *kubes*, that empower businesses to build and deploy highly scalable data platforms and AI models. Contributions are more than welcome.


