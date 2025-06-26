__all__ = ['APP_AUTHOR', 'APP_NAME', 'CONFIG_DIR']

from pathlib import Path

from platformdirs import user_config_dir

APP_NAME = 'music-player'
APP_AUTHOR = 'bennetr'
CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
