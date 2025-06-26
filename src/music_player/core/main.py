import asyncio
import logging
import sys

from music_player.core.music import ProviderPlugin
from music_player.core.plugin_manager import plugin_manager

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s: %(levelname)s | %(name)s] %(message)s', '%H:%M:%S')
handler.setFormatter(formatter)

root_logger.addHandler(handler)

logger = logging.getLogger('music_player.core.main')


async def main() -> None:
    """Main entry point of the application."""
    logger.info('Starting music player...')
    plugin_manager.load_plugins()

    tidal = plugin_manager.get(ProviderPlugin, 'ing.ranft.bennet.tidal').instance()
    login_result = await tidal.login()

    if login_result.result is True:
        logger.info('Successfully logged in')
    elif login_result.result is False:
        logger.error('Failed to log in')
    else:
        for strategy in login_result.strategies:
            logger.info('%s', strategy)

        result = await login_result.result

        if result:
            logger.info('Successfully logged in')
        else:
            logger.error('Failed to log in')


if __name__ == '__main__':
    asyncio.run(main())
