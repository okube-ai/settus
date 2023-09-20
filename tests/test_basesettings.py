import os
from pydantic import AliasChoices
from pydantic import ConfigDict
from settus import Field
from settus import BaseSettings

os.environ["MY_SECRET"] = "12345"
os.environ["ENV_1"] = "v1"
os.environ["TOP1"] = "t1"
os.environ["TOP2"] = "t2"


def test_basesettings():

    class Settings(BaseSettings):
        my_secret: str = ""
        your_secret: int = 25

    s = Settings()
    assert s.my_secret == "12345"
    assert s.your_secret == 25


def test_name_conflicts():

    class Settings(BaseSettings):
        s1: str = Field(default="s1")
        s2: str = Field(default="s2", alias="env_1")
        s3: str = Field(default="s2", alias=AliasChoices("env_2", "top1"))

    settings = Settings(s2="s2_from_init", s3="s3_from_init")
    assert settings.s2 == "s2_from_init"
    assert settings.s3 == "s3_from_init"

    class Settings2(BaseSettings):
        model_config = ConfigDict(populate_by_name=False, extra="forbid")
        s1: str = Field(default="s1")
        s2: str = Field(default="s2", alias="env_1")
        s3: str = Field(default="s2", alias=AliasChoices("top1", "top2"))

    settings = Settings2(env_1="s2_from_init", top2="s3_from_init")
    assert settings.s2 == "s2_from_init"
    assert settings.s3 == "s3_from_init"


if __name__ == "__main__":
    test_basesettings()
    test_name_conflicts()

