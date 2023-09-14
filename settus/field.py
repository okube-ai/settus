from pydantic import Field as _Field


def Field(*args, **kwargs):
    return _Field(*args, **kwargs)

