__all__ = ['UnknownPluginTypeError']

from typing import Any

from music_player.core.plugin_manager.plugin_definition import PluginDefinition


class UnknownPluginTypeError(TypeError):
    """Raised when trying to register a plugin that is not derived from a valid plugin class."""

    def __init__(self, plugin: PluginDefinition[Any]) -> None:
        """Initialize the error."""
        super().__init__(f'The plugin with the ID "{plugin.id}" is of an unknown type: {plugin.cls.__name__}.')
