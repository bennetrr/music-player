__all__ = ['BasePlugin']

from abc import ABC, abstractmethod

from .plugin_context import PluginContext


class BasePlugin(ABC):
    """Base class for a plugin."""

    _context: PluginContext

    @abstractmethod
    def __init__(self, context: PluginContext) -> None:
        """Initialize the plugin."""
        self._context = context

    @abstractmethod
    def close(self) -> None:
        """Clean up plugin resources."""
