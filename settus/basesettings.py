import pydantic
print("pydantic version", pydantic.__version__)
import pydantic_settings
print("pydantic settings version", pydantic_settings.__version__)

from pydantic_settings import BaseSettings as _BaseSettings


class BaseSettings(_BaseSettings):
    pass

