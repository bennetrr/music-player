from abc import ABC

from pydantic import BaseModel, PrivateAttr

from .base_plugin import BasePlugin
from .plugin_context import PluginContext


class PluginDefinition[TPlugin: BasePlugin](BaseModel, ABC):
    """
    Registration details for a plugin.

    :var id: A unique identifier for the plugin.
             To avoid conflicts, use the reverse domain format (e.g., ``com.example.plugin``).
    :var name: The display name of the plugin.
    :var icon: The icon URI of the plugin.
    :var cls: The plugin class.
    """

    id: str
    name: str
    icon: str
    cls: type[TPlugin]

    _instance: TPlugin | None = PrivateAttr(default=None)

    def close(self) -> None:
        """Clean up resources."""
        if self._instance is not None:
            self._instance.close()
            self._instance = None

    def instance(self) -> TPlugin:
        """Get the plugin instance."""
        if self._instance is None:
            context = PluginContext(self.id)
            self._instance = self.cls(context)

        return self._instance
