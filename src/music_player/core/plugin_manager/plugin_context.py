__all__ = ['PluginContext']

from asyncio import AbstractEventLoop, get_running_loop

from pydantic import BaseModel, ConfigDict


class PluginContext(BaseModel):
    """A plugin context contains all information a plugin needs at runtime, such as the config store."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: dict[str, str]
    credentials: dict[str, str]
    loop: AbstractEventLoop

    @classmethod
    def create(cls, plugin_id: str) -> 'PluginContext':
        """Create a new plugin context."""
        return cls(config={}, credentials={}, loop=get_running_loop())
