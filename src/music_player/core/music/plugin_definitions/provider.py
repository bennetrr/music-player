from music_player.core.music import Provider
from music_player.core.plugin_manager import PluginDefinition


class ProviderPlugin(PluginDefinition[Provider]):
    """
    Plugin definition for a provider.

    :var needs_login:
    """

    needs_login: bool
