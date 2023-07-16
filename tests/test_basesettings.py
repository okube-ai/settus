import os

from settus import BaseSettings

os.environ["MY_SECRET"] = "12345"


class Settings(BaseSettings):
    my_secret: str = ""
    your_secret: int = 25


def test_basesettings():
    s = Settings()
    assert s.my_secret == "12345"
    assert s.your_secret == 25


if __name__ == "__main__":
    test_basesettings()
