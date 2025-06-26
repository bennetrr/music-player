__all__ = ['PluginContext']

from asyncio import AbstractEventLoop

from pydantic import BaseModel, ConfigDict


class PluginContext(BaseModel):
    """A plugin context contains all information a plugin needs at runtime, such as the config store."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: dict[str, str]
    credentials: dict[str, str]
    loop: AbstractEventLoop
