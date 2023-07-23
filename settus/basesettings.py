import pydantic
print("pydantic version in venv", pydantic.__version__)
import pydantic_settings
print("pydantic settings version in venv", pydantic_settings.__version__)

from pydantic_settings import BaseSettings as _BaseSettings


class BaseSettings(_BaseSettings):
    pass

