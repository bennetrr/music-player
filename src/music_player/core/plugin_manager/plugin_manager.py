__all__ = ['plugin_manager']

from collections.abc import Iterator
from importlib import import_module
from logging import getLogger
from pkgutil import ModuleInfo, iter_modules
from typing import Any, cast

import music_player.plugin
from music_player.core.plugin_manager import PluginAlreadyRegisteredError, PluginDefinition
from music_player.core.plugin_manager.exceptions import UnknownPluginTypeError

logger = getLogger(__name__)


def _iter_namespace(namespace_pkg: Any) -> Iterator[ModuleInfo]:  # noqa: ANN401
    return iter_modules(namespace_pkg.__path__, namespace_pkg.__name__ + '.')


class PluginManager:
    """
    The plugin manager is responsible for loading and managing plugins.

    Each plugin must be in the ``music_player.plugin`` namespace and have a ``__init__.py`` file,
    which registers all plugin classes in the plugin manager.
    """

    _plugins_by_id: dict[str, PluginDefinition[Any]]
    _plugins_by_cls: dict[type[Any], list[PluginDefinition[Any]]]

    def __init__(self) -> None:
        """Initialize the plugin manager."""
        self._plugins_by_id = {}
        self._plugins_by_cls = {}

    @staticmethod
    def load_plugins() -> None:
        """Load all plugins in the ``music_player.plugin`` namespace."""
        plugins: list[str] = [name for _, name, _ in _iter_namespace(music_player.plugin)]
        logger.info('Found %d plugins: %s', len(plugins), plugins)

        for plugin in plugins:
            import_module(plugin)

    def register(self, plugin: PluginDefinition[Any]) -> None:
        """
        Register a plugin.

        :throws PluginAlreadyRegisteredError: If a plugin with the same ID was already registered.
        :throws UnknownPluginTypeError: If a plugin with an unknown type was registered.
        """
        if plugin.id in self._plugins_by_id:
            raise PluginAlreadyRegisteredError(plugin)

        for baseclass in self._plugins_by_cls:
            if issubclass(plugin.cls, baseclass):
                self._plugins_by_cls[baseclass].append(plugin)
                self._plugins_by_id[plugin.id] = plugin
                return

        raise UnknownPluginTypeError(plugin)

    def get[TPlugin: PluginDefinition[Any]](self, t: type[TPlugin], plugin_id: str) -> TPlugin:  # noqa: ARG002
        """
        Get the plugin with the given ID.

        :var t: The type of the plugin.
        :var plugin_id: The ID of the plugin.
        """
        return cast('TPlugin', self._plugins_by_id[plugin_id])


plugin_manager = PluginManager()
"""
The plugin manager is responsible for loading and managing plugins.

Each plugin must be in the ``music_player.plugin`` namespace and have a ``__init__.py`` file,
which registers all plugin classes in the plugin manager.
"""
