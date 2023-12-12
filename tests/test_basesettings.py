import os
import pytest
from pydantic import AliasChoices
from pydantic import ConfigDict
from settus import Field
from settus import BaseSettings

os.environ["MY_SECRET"] = "12345"
os.environ["E1"] = "v1"
os.environ["E2"] = "v2"
os.environ["E3"] = "10"


def test_basesettings():
    class Settings(BaseSettings):
        my_secret: str = ""
        your_secret: int = 25

    s = Settings()
    assert s.my_secret == "12345"
    assert s.your_secret == 25


def test_name_conflicts():
    class Settings1(BaseSettings):
        """
        Two settings sharing the same env var should have the same value.
        """

        s1: str = Field(default="s1", alias="e1")
        s2: str = Field(default="s2", alias="e1")

    settings = Settings1()
    assert settings.s1 == "v1"
    assert settings.s2 == "v1"

    # Source priority
    settings = Settings1(s1="i1")
    assert settings.s1 == "i1"
    assert settings.s2 == "v1"

    class Settings2(BaseSettings):
        """
        List alias choices are accounted in order
        """

        s1: str = Field(default="s1", alias="e1")
        s2: str = Field(default="s2", alias=AliasChoices("e2", "e1"))
        s3: str = Field(default="s3", alias=AliasChoices("e2", "e1"))

    settings = Settings2(s3="i3")
    assert settings.s1 == "v1"
    assert settings.s2 == "v2"
    assert settings.s3 == "i3"

    # Input alias should not be allowed to avoid conflict and generate exception
    with pytest.raises(AttributeError):
        Settings2(e1="i1", s3="i3")

    # Input alias should not be allowed to avoid conflict and generate exception
    with pytest.raises(ValueError):

        class Settings3(BaseSettings):
            """
            List alias choices are accounted in order
            """

            model_config = ConfigDict(populate_by_name=False)
            s1: str = Field(default="s1", alias="e1")

        Settings3()


def test_type_cast():
    class Settings(BaseSettings):
        s1: str = Field(default="s1", alias="e3")
        s2: int = Field(default="s2", alias="e3")

    settings = Settings()
    assert isinstance(settings.s1, str)
    assert isinstance(settings.s2, int)


if __name__ == "__main__":
    test_basesettings()
    test_name_conflicts()
    test_type_cast()
