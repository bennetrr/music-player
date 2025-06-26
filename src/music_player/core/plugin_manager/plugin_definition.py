from abc import ABC

from pydantic import BaseModel


class PluginDefinition[TPlugin: object](BaseModel, ABC):
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

    _instance: TPlugin | None

    def instance(self) -> TPlugin:
        """Get the plugin instance."""
        if self._instance is None:
            self._instance = self.cls()
        return self._instance
