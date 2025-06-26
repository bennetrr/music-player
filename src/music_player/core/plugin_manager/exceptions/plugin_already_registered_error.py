__all__ = ['PluginAlreadyRegisteredError']

from typing import Any

from music_player.core.plugin_manager.plugin_definition import PluginDefinition


class PluginAlreadyRegisteredError(ValueError):
    """Raised when trying to register a plugin with an ID that is already registered."""

    def __init__(self, plugin: PluginDefinition[Any]) -> None:
        """Initialize the error."""
        super().__init__(f'A plugin with the ID "{plugin.id}" is already registered.')
