import os

from pydantic import AliasChoices

from settus import BaseSettings
from settus import Field
from settus import SettingsConfigDict

os.environ["ENV_1"] = "v1"

KEYVAULT_URL = "https://o3-kv-settus-dev.vault.azure.net/"


def test_keyvault():
    try:
        import azure
    except ModuleNotFoundError:
        return

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(keyvault_url=KEYVAULT_URL)
        env_1: str = Field(default="undefined")
        top: str = Field(default="undefined")
        kv_1: str = Field(default="undefined", alias="my-secret")
        kv_2: str = Field(
            default="undefined", alias=AliasChoices("not-my-secret", "my-secret")
        )
        kv_3: str = Field(
            default="undefined", alias="my-secret", keyvault_url=KEYVAULT_URL
        )
        kv_4: str = Field(default="undefined", alias=AliasChoices("not-my-secret"))

    settings = Settings()
    assert settings.env_1 == "v1"
    assert settings.top == "topsecret"
    assert settings.kv_1 == "secretsauce"
    assert settings.kv_2 == "secretsauce"
    assert settings.kv_3 == "secretsauce"
    assert settings.kv_4 == "undefined"


if __name__ == "__main__":
    test_keyvault()
