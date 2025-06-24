__all__ = ['PluginContext']

from asyncio import AbstractEventLoop

from pydantic import BaseModel


class PluginContext(BaseModel):
    """A plugin context contains all information a plugin needs at runtime, such as the config store."""

    config: dict
    credentials: dict
    loop: AbstractEventLoop
