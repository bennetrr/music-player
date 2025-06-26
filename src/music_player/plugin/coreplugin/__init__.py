from music_player.core.music import ProviderPlugin
from music_player.core.plugin_manager import plugin_manager
from music_player.plugin.coreplugin.providers.tidal import TidalProvider

plugin_manager.register(
    ProviderPlugin(id='ing.ranft.bennet.tidal', name='TIDAL', icon='', cls=TidalProvider, needs_login=True)
)
