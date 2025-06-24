__all__ = ['load_plugins', 'plugin_manager']

import logging
from collections.abc import Iterator
from importlib import import_module
from pkgutil import ModuleInfo, iter_modules
from typing import Any

import music_player.plugin

logger = logging.getLogger(__name__)


def _iter_namespace(namespace_pkg: Any) -> Iterator[ModuleInfo]:  # noqa: ANN401
    return iter_modules(namespace_pkg.__path__, namespace_pkg.__name__ + '.')


def load_plugins() -> None:
    """Load all plugins in the ``music_player.plugin`` namespace."""
    plugins: list[str] = [name for _, name, _ in _iter_namespace(music_player.plugin)]
    logger.info('Found %d plugins: %s', len(plugins), plugins)

    for plugin in plugins:
        import_module(plugin)


class _PluginManager:
    """
    The plugin manager is responsible for loading and managing plugins.

    Each plugin must be in the ``music_player.plugin`` namespace and have a ``__init__.py`` file,
    which registers all plugin classes in the plugin manager.
    """


plugin_manager = _PluginManager()
"""
The plugin manager is responsible for loading and managing plugins.

Each plugin must be in the ``music_player.plugin`` namespace and have a ``__init__.py`` file,
which registers all plugin classes in the plugin manager.
"""
