__all__ = ['PluginContext']

from asyncio import AbstractEventLoop, get_running_loop
from pathlib import Path

from pydantic import BaseModel

from music_player.core.constants import CONFIG_DIR


class PluginContext:
    """A plugin context contains all information a plugin needs at runtime, such as the plugin config."""

    plugin_id: str
    loop: AbstractEventLoop

    _config_dir: Path
    _config_file: Path
    _credentials_file: Path

    def __init__(self, plugin_id: str) -> None:
        """Initialize a new plugin context."""
        self.plugin_id = plugin_id
        self.loop = get_running_loop()

        self._config_dir = CONFIG_DIR / 'plugins' / plugin_id
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._config_file = self._config_dir / 'config.json'
        self._credentials_file = self._config_dir / 'credentials.json'

    def get_config[TConfig: BaseModel](self, config_type: type[TConfig]) -> TConfig | None:
        """Get the config for the plugin."""
        if not self._config_file.exists():
            return None

        with self._config_file.open('r', encoding='utf-8') as f:
            return config_type.model_validate_json(f.read())

    def set_config[TConfig: BaseModel](self, config: TConfig) -> None:
        """Set the config for the plugin."""
        with self._config_file.open('w', encoding='utf-8') as f:
            f.write(config.model_dump_json())

    def get_credentials[TCredentials: BaseModel](self, credentials_type: type[TCredentials]) -> TCredentials | None:
        """Get the credentials for the plugin."""
        if not self._credentials_file.exists():
            return None

        with self._credentials_file.open('r', encoding='utf-8') as f:
            return credentials_type.model_validate_json(f.read())

    def set_credentials[TCredentials: BaseModel](self, credentials: TCredentials) -> None:
        """Set the credentials for the plugin."""
        with self._credentials_file.open('w', encoding='utf-8') as f:
            f.write(credentials.model_dump_json())
