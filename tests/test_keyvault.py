import os

from pydantic import AliasChoices

from settus import BaseSettings
from settus import Field
from settus import SettingsConfigDict

os.environ["ENV_1"] = "v1"
os.environ["TOP"] = "v2"

KEYVAULT_URL = "https://kv-laktory-dev.vault.azure.net/"


def test_keyvault():

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(keyvault_url=KEYVAULT_URL)
        env_1: str = Field(default="undefined")
        top: str = Field(default="undefined")
        kv_1: str = Field(default="undefined", alias="my-secret")
        kv_2: str = Field(default="undefined", alias=AliasChoices("ENV_1", "my-secret"))
        kv_3: str = Field(default="undefined", alias="my-secret", keyvault_url=KEYVAULT_URL)

    settings = Settings()
    print(settings)
    assert settings.env_1 == "v1"
    assert settings.kv_1 == "secretsauce"
    assert settings.top == "v2"
    assert settings.kv_2 == "v1"


if __name__ == "__main__":
    test_keyvault()

